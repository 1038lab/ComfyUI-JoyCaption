import torch
from transformers import AutoProcessor, LlavaForConditionalGeneration, BitsAndBytesConfig
import folder_paths
from pathlib import Path
from PIL import Image
from torchvision.transforms import ToPILImage
import json
import gc
import os

class ModelLoadError(Exception):
    pass

def handle_model_error(e, cleanup_func=None):
    if cleanup_func:
        cleanup_func()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    raise ModelLoadError(f"Error loading model: {str(e)}")

def cleanup_model_resources(model=None, processor=None):
    if model is not None:
        del model
    if processor is not None:
        del processor
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

def validate_model_parameters(quantization, valid_modes):
    if quantization not in valid_modes:
        raise ValueError(f"Invalid quantization mode: {quantization}. Valid modes: {', '.join(valid_modes)}")

with open(Path(__file__).parent / "jc_data.json", "r", encoding="utf-8") as f:
    config = json.load(f)
    CAPTION_TYPE_MAP = config["caption_type_map"]
    EXTRA_OPTIONS = config["extra_options"]
    MEMORY_EFFICIENT_CONFIGS = config["memory_efficient_configs"]
    MODEL_SETTINGS = config["model_settings"]
    CAPTION_LENGTH_CHOICES = config["caption_length_choices"]
    HF_MODELS = config["hf_models"]

# --- Custom Models Merge Logic (for HF models only) ---
custom_path = Path(__file__).parent / "custom_models.json"

if custom_path.exists():
    try:
        with open(custom_path, "r", encoding="utf-8") as f:
            custom_data = json.load(f) or {}
        HF_MODELS.update(custom_data.get("hf_models", {}))
        print("[JoyCaption] ✅ Loaded custom HF custom models.")
    except Exception as e:
        print(f"[JoyCaption] ⚠️ Failed to load custom models → {e}")
else:
    print("[JoyCaption] ℹ️ No custom models found, skipping user-defined HF models.")
# ------------------------------------------------------

def build_prompt(caption_type: str, caption_length: str | int, extra_options: list[str], name_input: str) -> str:
    """Constructs the prompt for the model based on user selections."""
    if caption_length == "any":
        map_idx = 0
    elif isinstance(caption_length, str) and caption_length.isdigit():
        map_idx = 1
    else:
        map_idx = 2
    
    prompt = CAPTION_TYPE_MAP[caption_type][map_idx]

    if extra_options:
        prompt += " " + " ".join(extra_options)
    
    return prompt.format(
        name=name_input or "{NAME}",
        length=caption_length,
        word_count=caption_length,
    )

_MODEL_CACHE = {}

class JC_Models:
    """Handles loading, caching, and running the LLaVA models."""
    def __init__(self, model: str, memory_mode: str):
        cache_key = f"{model}_{memory_mode}"
        
        if cache_key in _MODEL_CACHE:
            try:
                self.processor = _MODEL_CACHE[cache_key]["processor"]
                self.model = _MODEL_CACHE[cache_key]["model"]
                self.device = _MODEL_CACHE[cache_key]["device"]
                if not next(self.model.parameters()).is_cuda:
                    raise RuntimeError("Cached model not on GPU")
                print(f"Using cached model: {cache_key}")
                return
            except Exception as e:
                print(f"Cache validation failed: {e}, reloading model...")
                if cache_key in _MODEL_CACHE:
                    del _MODEL_CACHE[cache_key]
                torch.cuda.empty_cache()
        
        checkpoint_path = Path(folder_paths.models_dir) / "LLM" / Path(model).stem
        if not checkpoint_path.exists():
            from huggingface_hub import snapshot_download
            snapshot_download(repo_id=model, local_dir=str(checkpoint_path), force_download=False, local_files_only=False)
        
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        if self.device == "cuda":
            torch.backends.cudnn.benchmark = True
            if hasattr(torch.backends, 'cuda'):
                if hasattr(torch.backends.cuda, 'matmul'):
                    torch.backends.cuda.matmul.allow_tf32 = True
                if hasattr(torch.backends.cuda, 'allow_tf32'):
                    torch.backends.cuda.allow_tf32 = True
            
            os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:128"
        
        self.processor = AutoProcessor.from_pretrained(
            str(checkpoint_path), 
            use_fast=True,
            image_processor_type="CLIPImageProcessor",
            image_size=336
        )

        if hasattr(self.processor, 'image_processor') and hasattr(self.processor.image_processor, 'size'):
            expected_size = self.processor.image_processor.size
            if isinstance(expected_size, dict):
                self.target_size = (expected_size.get('height', 336), expected_size.get('width', 336))
            elif isinstance(expected_size, (list, tuple)):
                self.target_size = tuple(expected_size) if len(expected_size) == 2 else (expected_size[0], expected_size[0])
            else:
                self.target_size = (expected_size, expected_size)
        else:
            self.target_size = (336, 336)

        model_kwargs = {
            "device_map": "cuda" if self.device == "cuda" else "cpu",
        }

        try:
            if "FP8-Dynamic" in model:
                print("Loading FP8 model with automatic configuration...")
                self.model = LlavaForConditionalGeneration.from_pretrained(
                    str(checkpoint_path),
                    torch_dtype="auto",
                    **model_kwargs
                )
            elif memory_mode == "Full Precision (bf16)":
                self.model = LlavaForConditionalGeneration.from_pretrained(
                    str(checkpoint_path), 
                    torch_dtype=torch.bfloat16,
                    **model_kwargs
                )
            elif memory_mode == "Balanced (8-bit)":
                qnt_config = BitsAndBytesConfig(
                    load_in_8bit=True,
                    bnb_8bit_compute_dtype=torch.float16,
                    bnb_8bit_use_double_quant=True,
                    llm_int8_skip_modules=["vision_tower", "multi_modal_projector"],
                    llm_int8_enable_fp32_cpu_offload=True
                )
                self.model = LlavaForConditionalGeneration.from_pretrained(
                    str(checkpoint_path), 
                    torch_dtype=torch.float16,
                    quantization_config=qnt_config,
                    **model_kwargs
                )
            else:
                qnt_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_use_double_quant=True,
                    llm_int8_skip_modules=["vision_tower", "multi_modal_projector"],
                    llm_int8_enable_fp32_cpu_offload=True
                )
                self.model = LlavaForConditionalGeneration.from_pretrained(
                    str(checkpoint_path), 
                    torch_dtype="auto",
                    quantization_config=qnt_config,
                    **model_kwargs
                )
            
            self.model.eval()
            
            if self.device == "cuda" and not next(self.model.parameters()).is_cuda:
                raise RuntimeError("Model failed to load on GPU")
            
            if memory_mode == "Global Cache":
                _MODEL_CACHE[cache_key] = {
                    "processor": self.processor,
                    "model": self.model,
                    "device": self.device
                }
                
        except Exception as e:
            cleanup_model_resources(self.model, self.processor)
            handle_model_error(e)
    
    @torch.inference_mode()
    def generate(self, image: Image.Image, system: str, prompt: str, max_new_tokens: int, temperature: float, top_p: float, top_k: int) -> str:
        """Generates a caption for the given image."""
        convo = [
            {"role": "system", "content": system.strip()},
            {"role": "user", "content": prompt.strip()},
        ]

        convo_string = self.processor.apply_chat_template(convo, tokenize=False, add_generation_prompt=True)
        assert isinstance(convo_string, str)

        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image = image.resize(self.target_size, Image.Resampling.LANCZOS)
        
        inputs = self.processor(text=[convo_string], images=[image], return_tensors="pt").to(self.device)
        
        if hasattr(inputs, 'pixel_values') and inputs['pixel_values'] is not None:
            inputs['pixel_values'] = inputs['pixel_values'].to(self.model.dtype)

        with torch.cuda.amp.autocast(enabled=True):
            generate_ids = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True if temperature > 0 else False,
                suppress_tokens=None,
                use_cache=True,
                temperature=temperature,
                top_k=None if top_k == 0 else top_k,
                top_p=top_p,
            )[0]

        generate_ids = generate_ids[inputs['input_ids'].shape[1]:]
        caption = self.processor.tokenizer.decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)
        return caption.strip()

class JC_ExtraOptions:
    """A node to collect extra options for captioning."""
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {"required": {}}
        for key, value in EXTRA_OPTIONS.items():
            inputs["required"][key] = ("BOOLEAN", {"default": value["default"]})
        inputs["required"]["character_name"] = ("STRING", {"default": "", "multiline": True, "placeholder": "Character Name"})
        return inputs

    RETURN_TYPES = ("JOYCAPTION_EXTRA_OPTIONS",)
    RETURN_NAMES = ("extra_options",)
    FUNCTION = "get_extra_options"
    CATEGORY = "🧪AILab/📝JoyCaption"

    def get_extra_options(self, character_name, **kwargs):
        ret_list = []
        for key, value in EXTRA_OPTIONS.items():
            if kwargs.get(key, False):
                ret_list.append(value["description"])
        return ([ret_list, character_name],)

class JC:
    """The main, simple JoyCaption node."""
    @classmethod
    def INPUT_TYPES(cls):
        model_list = list(HF_MODELS.keys())
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (model_list, {"default": model_list[1], "tooltip": "Select the AI model to use for caption generation"}),
                "quantization": (list(MEMORY_EFFICIENT_CONFIGS.keys()), {"default": "Balanced (8-bit)", "tooltip": "Choose between speed and quality. 8-bit is recommended for most users"}),
                "prompt_style": (list(CAPTION_TYPE_MAP.keys()), {"default": "Descriptive", "tooltip": "Select the style of caption you want to generate"}),
                "caption_length": (CAPTION_LENGTH_CHOICES, {"default": "any", "tooltip": "Control the length of the generated caption"}),
                "memory_management": (["Keep in Memory", "Clear After Run", "Global Cache"], {"default": "Keep in Memory", "tooltip": "Choose how to manage model memory. 'Keep in Memory' for faster processing, 'Clear After Run' for limited VRAM, 'Global Cache' for fastest processing if you have enough VRAM"}),
            },
            "optional": {
                "extra_options": ("JOYCAPTION_EXTRA_OPTIONS", {"tooltip": "Additional options to customize the caption generation"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "generate"
    CATEGORY = "🧪AILab/📝JoyCaption"

    def __init__(self):
        self.predictor = None
        self.current_memory_mode = None
        self.current_model = None
    
    def generate(self, image, model, quantization, prompt_style, caption_length, memory_management, extra_options=None):
        try:
            validate_model_parameters(quantization, list(MEMORY_EFFICIENT_CONFIGS.keys()))
            
            if memory_management == "Global Cache":
                try:
                    model_name = HF_MODELS[model]["name"]
                    self.predictor = JC_Models(model_name, quantization)
                except Exception as e:
                    return (f"Error loading model: {e}",)
            elif self.predictor is None or self.current_memory_mode != quantization or self.current_model != model:
                if self.predictor is not None:
                    del self.predictor
                    self.predictor = None
                    torch.cuda.empty_cache()
                    gc.collect()
                try:
                    model_name = HF_MODELS[model]["name"]
                    self.predictor = JC_Models(model_name, quantization)
                    self.current_memory_mode = quantization
                    self.current_model = model
                except Exception as e:
                    return (f"Error loading model: {e}",)

            prompt = build_prompt(prompt_style, caption_length, extra_options[0] if extra_options else [], extra_options[1] if extra_options else "{NAME}")
            system_prompt = MODEL_SETTINGS["default_system_prompt"]
            pil_image = ToPILImage()(image[0].permute(2, 0, 1))
            
            response = self.predictor.generate(
                image=pil_image,
                system=system_prompt,
                prompt=prompt,
                max_new_tokens=MODEL_SETTINGS["default_max_tokens"],
                temperature=MODEL_SETTINGS["default_temperature"],
                top_p=MODEL_SETTINGS["default_top_p"],
                top_k=MODEL_SETTINGS["default_top_k"],
            )

            if memory_management == "Clear After Run":
                del self.predictor
                self.predictor = None
                torch.cuda.empty_cache()
                gc.collect()

            return (response,)
        except Exception as e:
            if memory_management == "Clear After Run":
                del self.predictor
                self.predictor = None
                torch.cuda.empty_cache()
                gc.collect()
            raise e

class JC_adv:
    """The advanced JoyCaption node with more settings."""
    @classmethod
    def INPUT_TYPES(cls):
        model_list = list(HF_MODELS.keys())
        return {
            "required": {
                "image": ("IMAGE",),
                "model": (model_list, {"default": model_list[1], "tooltip": "Select the AI model to use for caption generation"}),
                "quantization": (list(MEMORY_EFFICIENT_CONFIGS.keys()), {"default": "Balanced (8-bit)", "tooltip": "Choose between speed and quality. 8-bit is recommended for most users"}),
                "prompt_style": (list(CAPTION_TYPE_MAP.keys()), {"default": "Descriptive", "tooltip": "Select the style of caption you want to generate"}),
                "caption_length": (CAPTION_LENGTH_CHOICES, {"default": "any", "tooltip": "Control the length of the generated caption"}),
                "max_new_tokens": ("INT", {"default": MODEL_SETTINGS["default_max_tokens"], "min": 1, "max": 2048, "tooltip": "Maximum number of tokens to generate. Higher values allow longer captions"}),
                "temperature": ("FLOAT", {"default": MODEL_SETTINGS["default_temperature"], "min": 0.0, "max": 2.0, "step": 0.05, "tooltip": "Control the randomness of the output. Higher values make the output more creative but less predictable"}),
                "top_p": ("FLOAT", {"default": MODEL_SETTINGS["default_top_p"], "min": 0.0, "max": 1.0, "step": 0.01, "tooltip": "Control the diversity of the output. Higher values allow more diverse word choices"}),
                "top_k": ("INT", {"default": MODEL_SETTINGS["default_top_k"], "min": 0, "max": 100, "tooltip": "Limit the number of possible next tokens. Lower values make the output more focused"}),
                "custom_prompt": ("STRING", {"default": "", "multiline": True, "tooltip": "Custom prompt template. If empty, will use the selected prompt style"}),
                "memory_management": (["Keep in Memory", "Clear After Run", "Global Cache"], {"default": "Keep in Memory", "tooltip": "Choose how to manage model memory. 'Keep in Memory' for faster processing, 'Clear After Run' for limited VRAM, 'Global Cache' for fastest processing if you have enough VRAM"}),
            },
            "optional": {
                "extra_options": ("JOYCAPTION_EXTRA_OPTIONS", {"tooltip": "Additional options to customize the caption generation"}),
            }
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("PROMPT", "STRING")
    FUNCTION = "generate"
    CATEGORY = "🧪AILab/📝JoyCaption"

    def __init__(self):
        self.predictor = None
        self.current_memory_mode = None
        self.current_model = None
    
    def generate(self, image, model, quantization, prompt_style, caption_length, max_new_tokens, temperature, top_p, top_k, custom_prompt, memory_management, extra_options=None):
        try:
            validate_model_parameters(quantization, list(MEMORY_EFFICIENT_CONFIGS.keys()))
            
            if memory_management == "Global Cache":
                try:
                    model_name = HF_MODELS[model]["name"]
                    self.predictor = JC_Models(model_name, quantization)
                except Exception as e:
                    return (f"Error loading model: {e}", "")
            elif self.predictor is None or self.current_memory_mode != quantization or self.current_model != model:
                if self.predictor is not None:
                    del self.predictor
                    self.predictor = None
                    torch.cuda.empty_cache()
                    gc.collect()
                try:
                    model_name = HF_MODELS[model]["name"]
                    self.predictor = JC_Models(model_name, quantization)
                    self.current_memory_mode = quantization
                    self.current_model = model
                except Exception as e:
                    return (f"Error loading model: {e}", "")

            if custom_prompt and custom_prompt.strip():
                prompt = custom_prompt.strip()
            else:
                prompt = build_prompt(prompt_style, caption_length, extra_options[0] if extra_options else [], extra_options[1] if extra_options else "{NAME}")
            
            system_prompt = MODEL_SETTINGS["default_system_prompt"]
            pil_image = ToPILImage()(image[0].permute(2, 0, 1))
            
            response = self.predictor.generate(
                image=pil_image,
                system=system_prompt,
                prompt=prompt,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
            )

            if memory_management == "Clear After Run":
                del self.predictor
                self.predictor = None
                torch.cuda.empty_cache()
                gc.collect()

            return (prompt, response)
        except Exception as e:
            if memory_management == "Clear After Run":
                del self.predictor
                self.predictor = None
                torch.cuda.empty_cache()
                gc.collect()
            raise e

NODE_CLASS_MAPPINGS = {
    "JC": JC,
    "JC_adv": JC_adv,
    "JC_ExtraOptions": JC_ExtraOptions,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JC": "JoyCaption",
    "JC_adv": "JoyCaption (Advanced)",
    "JC_ExtraOptions": "JoyCaption Extra Options",
}

