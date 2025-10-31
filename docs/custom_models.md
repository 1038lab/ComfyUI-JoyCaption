# 🧩 JoyCaption Custom Models Guide
Supports both **HF** and **GGUF** model customization.

---

## 💡 Overview
Starting from **JoyCaption v2.0.2**, users can register **their own models** —  
without modifying any of the repository’s internal configuration files.

This makes it easy to:
- Test your own LLaVA / Phi / Qwen / Mistral etc. models  
- Add new quantized GGUF models  
- Keep your changes persistent between JoyCaption updates  

---

## 📁 File Location
Create or edit this file in your JoyCaption directory:

```

ComfyUI/custom_nodes/ComfyUI-JoyCaption/custom_models.json

````

If the file doesn’t exist, JoyCaption will **skip it safely** (no errors).  
You can also copy the provided `custom_models_example.json` and rename it.

---

## ⚙️ File Structure

```json
{
  "hf_models": {
    "My-LLaVA-Model": {
      "name": "myusername/llava-custom-model",
      "description": "Example Hugging Face model for JoyCaption (HF format)."
    }
  },
  "gguf_models": {
    "My-GGUF-Caption-Model": {
      "name": "myusername/llava-custom-gguf/model.gguf",
      "description": "Example GGUF model with image captioning support."
    }
  }
}
````

### 🧱 Explanation

| Key           | Description                                                           |
| ------------- | --------------------------------------------------------------------- |
| `hf_models`   | Models loaded through HuggingFace / Transformers (used by `JC.py`)    |
| `gguf_models` | Models using llama.cpp GGUF format (used by `JC_GGUF.py`)             |
| `name`        | Model identifier — either full HF repo path or local `.gguf` filename |
| `description` | Optional. Appears as tooltip in ComfyUI node interface                |

---

## 🧩 Empty Default File

For users who haven’t added anything yet,
you can safely ship this minimal empty version in the repo:

```json
{
  "hf_models": {},
  "gguf_models": {}
}
```

If the file is empty or missing, JoyCaption will continue using built-in models.

---

## 🧱 Example Template

An example file `custom_models_example.json` is provided in the repository root:

```json
{
  "__comment__": "Example for user customization",
  "hf_models": {
    "My-Phi-Vision": {
      "name": "myusername/phi-vision-captioner",
      "description": "Custom Phi-based visual captioning model."
    }
  },
  "gguf_models": {
    "My-Gemma-GGUF": {
      "name": "mlabonne/gemma-3-27b-it-abliterated-GGUF",
      "description": "High-quality GGUF model for image captioning."
    }
  }
}
```

Rename this file to `custom_models.json` to activate it.

---

## 🧰 Behavior Notes

* ✅ The system merges your `custom_models.json` entries with internal presets.
* ⚙️ The merging happens **at runtime** — no need to modify `jc_data.json`.
* 🧼 Safe: if parsing fails, JoyCaption prints a warning and continues running.
* 🔒 Your file is ignored during updates (no overwriting by git pulls).
* 🖥️ Works for both `JC.py` and `JC_GGUF.py` independently.

---

## 📘 Related Files

| File                         | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| `JC.py`                      | Handles HF-based models (e.g., LLaVA, Phi, Qwen) |
| `JC_GGUF.py`                 | Handles quantized GGUF models                    |
| `custom_models.json`         | Your personal model definitions                  |
| `custom_models_example.json` | Example reference file                           |

---

## 🧠 Tips for Power Users

* You can define **multiple entries** under each section.
* Hugging Face repos can include **subfolders or filenames** if needed:

  ```
  "name": "myrepo/models/llava-custom-4bit/ggml-model-q4_k.gguf"
  ```
* For local models, use the **relative path** under your `ComfyUI/models` directory.
* Descriptions are optional but highly recommended.

---

## 🪄 Troubleshooting

| Issue                                       | Possible Cause                                        | Fix                                          |
| ------------------------------------------- | ----------------------------------------------------- | -------------------------------------------- |
| Model not showing in dropdown               | JSON syntax error or missing section                  | Validate JSON format                         |
| “Failed to load custom_models.json” warning | Invalid JSON content                                  | Check braces/quotes                          |
| Model loads but errors on inference         | Wrong path or unsupported format                      | Verify `name` path and model type            |
| GGUF model missing mmproj                   | Ensure `GGUF_SETTINGS["mmproj_filename"]` file exists | Download via `hf_hub_download` automatically |

---

## 🏁 Summary

✅ **No internal edits needed**
✅ **Both HF and GGUF supported**
✅ **Safe and optional**
✅ **Updatable without conflicts**

