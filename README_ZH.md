# ComfyUI-JoyCaption

[English](README.md) | [简体中文](README_ZH.md)

ComfyUI 自定义节点，基于 LLaVA VLM 提供高级图像描述功能，支持自定义风格和内存优化推理。

## 功能特点

- 简单友好的用户界面
- 支持多种描述类型
- 灵活的长度控制
- 内存优化选项
- **GGUF 模型支持** - 高效的量化模型，提供更好的性能和更低的内存使用
- **自动模型下载** - 首次使用时自动下载并正确重命名模型
- 支持多种描述类型
- 支持高级自定义选项
- 多种精度选项 (fp32, bf16, fp16, 8-bit, 4-bit)
- 增强的内存管理，支持全局缓存模式
- 干净的控制台输出（无调试垃圾信息）
- 强大的错误处理和参数验证
- **llama_cpp_install文件夹** - 完整的llama-cpp-python安装指南和自动化脚本

## 安装

1. 将此仓库克隆到您的 `ComfyUI/custom_nodes` 目录：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/1038lab/ComfyUI-JoyCaption.git
```

2. 安装所需依赖：
```bash
cd ComfyUI/custom_nodes/ComfyUI-JoyCaption
pip install -r requirements.txt
```

3. **GGUF模型（推荐）**: 安装支持CUDA的llama-cpp-python：
```bash
# 选项1: 自动化安装（推荐）
python llama_cpp_install/llama_cpp_install.py

# 选项2: 手动安装
pip install -r requirements_gguf.txt
```

**可用安装指南:**
- **English**: [llama_cpp_install/llama_cpp_install.md](llama_cpp_install/llama_cpp_install.md)
- **中文**: [llama_cpp_install/llama_cpp_install_zh.md](llama_cpp_install/llama_cpp_install_zh.md)

## 下载模型
模型将在首次使用时自动下载并重命名，或者您可以手动下载：

### 标准模型（HuggingFace 格式）
| 模型 | 链接 | 内存使用 |
| ----- | ---- | ------------ |
| JoyCaption Beta One | [下载](https://huggingface.co/fancyfeast/llama-joycaption-beta-one-hf-llava) | ~8-16GB |
| JoyCaption Alpha Two | [下载](https://huggingface.co/fancyfeast/llama-joycaption-alpha-two-hf-llava) | ~8-16GB |

### GGUF 模型（量化，推荐）
| 模型 | 大小 | 内存使用 | 质量 | 推荐用途 | 链接 |
| ----- | ---- | ------------ | ------- | --------------- | ---- |
| JoyCaption Beta One (Q2_K) | 3.18GB | ~4GB | 良好 | 低显存 (6GB+) | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q2_K.gguf) |
| JoyCaption Beta One (Q3_K_S) | 3.66GB | ~5GB | 良好+ | 预算系统 (8GB+) | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q3_K_S.gguf) |
| JoyCaption Beta One (Q3_K_M) | 4.02GB | ~5GB | 更好 | 平衡性能 | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q3_K_M.gguf) |
| JoyCaption Beta One (Q3_K_L) | 4.32GB | ~6GB | 更好+ | 质量/大小平衡 | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q3_K_L.gguf) |
| JoyCaption Beta One (IQ4_XS) | 4.48GB | ~6GB | 很好 | **推荐** (8GB+) | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.IQ4_XS.gguf) |
| JoyCaption Beta One (Q4_K_S) | 4.69GB | ~6GB | 很好 | 质量导向 | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q4_K_S.gguf) |
| JoyCaption Beta One (Q4_K_M) | 4.92GB | ~7GB | 很好+ | 平衡选择 | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q4_K_M.gguf) |
| JoyCaption Beta One (Q5_K_S) | 5.60GB | ~7GB | 优秀 | 高质量 (10GB+) | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q5_K_S.gguf) |
| JoyCaption Beta One (Q5_K_M) | 5.73GB | ~8GB | 优秀+ | 高端质量 | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q5_K_M.gguf) |
| JoyCaption Beta One (Q6_K) | 6.60GB | ~8GB | 接近原版 | 最高质量 (12GB+) | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q6_K.gguf) |
| JoyCaption Beta One (Q8_0) | 8.54GB | ~10GB | 原版- | 全精度替代 | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.Q8_0.gguf) |
| JoyCaption Beta One (F16) | 16.1GB | ~18GB | 原版 | 全精度 (24GB+) | [下载](https://huggingface.co/mradermacher/llama-joycaption-beta-one-hf-llava-GGUF/resolve/main/llama-joycaption-beta-one-hf-llava.f16.gguf) |

#### 备选 GGUF 源
| 模型 | 大小 | 来源 | 链接 |
| ----- | ---- | ------ | ---- |
| JoyCaption Beta One (Q4_K) | 4.92GB | concedo | [下载](https://huggingface.co/concedo/llama-joycaption-beta-one-hf-llava-mmproj-gguf/resolve/main/Llama-Joycaption-Beta-One-Hf-Llava-Q4_K.gguf) |
| JoyCaption Beta One (Q8_0) | 8.54GB | concedo | [下载](https://huggingface.co/concedo/llama-joycaption-beta-one-hf-llava-mmproj-gguf/resolve/main/Llama-Joycaption-Beta-One-Hf-Llava-Q8_0.gguf) |
| JoyCaption Beta One (F16) | 16.1GB | concedo | [下载](https://huggingface.co/concedo/llama-joycaption-beta-one-hf-llava-mmproj-gguf/resolve/main/Llama-Joycaption-Beta-One-Hf-Llava-F16.gguf) |

**注意**：GGUF 模型还需要视觉投影模型：
- [llama-joycaption-beta-one-llava-mmproj-model-f16.gguf](https://huggingface.co/concedo/llama-joycaption-beta-one-hf-llava-mmproj-gguf/resolve/main/llama-joycaption-beta-one-llava-mmproj-model-f16.gguf)

下载后，将模型文件放置在 `ComfyUI/models/LLM/GGUF` 目录中。

## 基本使用

### 标准节点（HuggingFace 模型）

#### 基础节点
1. 从 `🧪AILab/📝JoyCaption` 类别添加 "JoyCaption" 节点
2. 将图像源连接到节点
3. 选择模型文件（默认为 `llama-joycaption-beta-one-hf-llava`）
4. 根据需要调整参数
5. 运行工作流

#### 高级节点
1. 从 `🧪AILab/📝JoyCaption` 类别添加 "JoyCaption (Advanced)" 节点
2. 将图像源连接到节点
3. 选择描述类型
4. 根据需要调整参数
5. 运行工作流

### GGUF 节点（推荐，性能更佳）

#### GGUF 基础节点
1. 从 `🧪AILab/📝JoyCaption-GGUF` 类别添加 "JoyCaption GGUF" 节点
2. 将图像源连接到节点
3. 选择 GGUF 模型（例如 "JoyCaption Beta One (IQ4_XS)"）
4. 选择处理模式（GPU/CPU）
5. 选择描述风格和长度
6. 运行工作流

#### GGUF 高级节点
1. 从 `🧪AILab/📝JoyCaption-GGUF` 类别添加 "JoyCaption GGUF (Advanced)" 节点
2. 将图像源连接到节点
3. 配置所有生成参数（temperature、top_p、top_k 等）
4. 如需要可设置自定义提示
5. 运行工作流

## 描述工具

### 图像批处理路径 🖼️

此节点允许您从目录中加载多个图像进行批处理：

| 参数 | 描述 |
| --------- | ----------- |
| **image_dir** | 包含图像的目录路径 |
| **batch_size** | 要加载的图像数量（0 = 所有图像） |
| **start_from** | 从第N张图像开始（1 = 第一张图像） |
| **sort_method** | 图像加载顺序：顺序/倒序/随机 |

### 描述保存器 📝

此节点将生成的描述保存到文本文件：

| 参数 | 描述 |
| --------- | ----------- |
| **string** | 要保存的描述文本 |
| **image_path** | 被描述图像的路径 |
| **image** | （可选）要与描述一起保存的图像 |
| **custom_output_path** | （可选）自定义输出目录路径 |
| **custom_file_name** | （可选）自定义文件名（不带扩展名） |
| **overwrite** | 如果为true，将覆盖现有文件；如果为false，将添加数字使文件名唯一 |

### 参数说明

#### 标准节点

##### 基础节点
| 参数 | 描述 | 默认值 | 范围 |
| --------- | ----------- | ------- | ----- |
| **Model** | 使用的 JoyCaption 模型 | `llama-joycaption-beta-one-hf-llava` | - |
| **Memory Control** | 内存优化设置 | Default | Default (fp32), Balanced (8-bit), Maximum Savings (4-bit) |
| **Caption Type** | 描述风格选择 | Descriptive | Descriptive, Descriptive (Casual), Straightforward, Tags, Technical, Artistic |
| **Caption Length** | 输出长度控制 | medium | any, very short, short, medium, long, very long |

#### GGUF 节点

##### GGUF 基础节点
| 参数 | 描述 | 默认值 | 范围 |
| --------- | ----------- | ------- | ----- |
| **Model** | 使用的 GGUF 模型 | JoyCaption Beta One (IQ4_XS) | Q2_K, IQ4_XS, Q5_K_M, Q6_K |
| **Processing Mode** | 硬件加速 | GPU | GPU, CPU |
| **Caption Type** | 描述风格选择 | Descriptive | Descriptive, Descriptive (Casual), Straightforward, Tags, Technical, Artistic |
| **Caption Length** | 输出长度控制 | any | any, very short, short, medium, long, very long |
| **Memory Management** | 模型内存处理 | Keep in Memory | Keep in Memory, Clear After Run, Global Cache |

##### GGUF 高级节点
| 参数 | 描述 | 默认值 | 范围 |
| --------- | ----------- | ------- | ----- |
| **Model** | 使用的 GGUF 模型 | JoyCaption Beta One (IQ4_XS) | Q2_K, IQ4_XS, Q5_K_M, Q6_K |
| **Processing Mode** | 硬件加速 | GPU | GPU, CPU |
| **Max New Tokens** | 最大生成标记数 | 512 | 1-2048 |
| **Temperature** | 生成随机性 | 0.6 | 0.0-2.0 |
| **Top-p** | 核采样 | 0.9 | 0.0-1.0 |
| **Top-k** | Top-k 采样 | 0 | 0-100 |
| **Custom Prompt** | 自定义提示模板 | "" | 任意文本 |
| **Memory Management** | 模型内存处理 | Keep in Memory | Keep in Memory, Clear After Run, Global Cache |

### 量化选项

#### 标准模型（HuggingFace）
| 模式 | 精度 | 内存使用 | 速度 | 质量 | 推荐 GPU |
|------|-----------|--------------|-------|---------|----------------|
| Default | fp32 | ~16GB | 1x | 最佳 | 24GB+ |
| Default | bf16 | ~8GB | 1.5x | 优秀 | 16GB+ |
| Default | fp16 | ~8GB | 2x | 很好 | 16GB+ |
| Balanced | 8-bit | ~4GB | 2.5x | 良好 | 12GB+ |
| Maximum Savings | 4-bit | ~2GB | 3x | 可接受 | 8GB+ |

#### GGUF 模型（推荐）
| 量化 | 模型大小 | 内存使用 | 速度 | 质量 | 推荐 GPU |
|-------------|------------|--------------|-------|---------|----------------|
| Q2_K | 3.18GB | ~4GB | 4x | 良好 | 6GB+ |
| Q3_K_S | 3.66GB | ~5GB | 3.5x | 良好+ | 8GB+ |
| Q3_K_M | 4.02GB | ~5GB | 3.5x | 更好 | 8GB+ |
| Q3_K_L | 4.32GB | ~6GB | 3x | 更好+ | 8GB+ |
| IQ4_XS | 4.48GB | ~6GB | 3x | 很好 | 8GB+ |
| Q4_K_S | 4.69GB | ~6GB | 3x | 很好 | 8GB+ |
| Q4_K_M | 4.92GB | ~7GB | 2.5x | 很好+ | 10GB+ |
| Q5_K_S | 5.60GB | ~7GB | 2.5x | 优秀 | 10GB+ |
| Q5_K_M | 5.73GB | ~8GB | 2.5x | 优秀+ | 12GB+ |
| Q6_K | 6.60GB | ~8GB | 2x | 接近原版 | 12GB+ |
| Q8_0 | 8.54GB | ~10GB | 1.8x | 原版- | 16GB+ |
| F16 | 16.1GB | ~18GB | 1.5x | 原版 | 24GB+ |

**注意**：GGUF 模型相比标准模型提供更好的性能和更低的内存使用。IQ4_XS 提供质量和效率的最佳平衡。

#### 高级节点

| 参数 | 描述 | 默认值 | 范围 |
| --------- | ----------- | ------- | ----- |
| **Extra Options** | 额外功能选项 | [] | 多个选项 |
| **Person Name** | 人物描述名称 | "" | 任意文本 |
| **Max New Tokens** | 最大生成标记数 | 512 | 1-2048 |
| **Temperature** | 生成温度 | 0.6 | 0.0-2.0 |
| **Top-p** | 采样参数 | 0.9 | 0.0-1.0 |
| **Top-k** | Top-k 采样 | 0 | 0-100 |

### 内存管理选项

| 模式 | 描述 | 推荐使用 |
|------|-------------|-----------------|
| 全局缓存 | 将模型保持在内存中以获得最快的处理速度 | 高显存 GPU (16GB+) |
| 保持内存 | 在工作流结束前保持模型在内存中 | 中等显存 GPU (8GB+) |
| 运行后清除 | 每次生成后清除模型 | 低显存 GPU (<8GB) |

## 设置建议

| 设置 | 建议 |
| ------- | -------------- |
| **模型选择** | 使用 GGUF 模型获得更好的性能和更低的内存使用。IQ4_XS 提供质量和效率的最佳平衡 |
| **内存模式** | 根据 GPU 显存：24GB+ 使用全局缓存，12GB+ 使用保持内存，8GB+ 使用运行后清除 |
| **处理模式** | 使用 GPU 模式获得更快处理速度，CPU 模式适用于显存有限的系统 |
| **输入分辨率** | 模型最适合 512x512 或更高分辨率的图像 |
| **内存使用** | 如果遇到内存问题，尝试 GGUF Q2_K 模型或使用运行后清除模式 |
| **性能** | 对于批处理，如果有足够的显存，考虑使用 GGUF 模型的全局缓存模式 |
| **Temperature** | 较低值 (0.6-0.7) 获得更稳定的结果，较高值 (0.8-1.0) 获得更多样化的结果 |
| **Top-k 参数** | 设置为 0 禁用，或使用 40-50 等值获得更集中的生成 |

## 关于模型

本实现使用基于 LLaVA 的图像描述模型，经过优化以提供快速准确的图像描述。

模型特点：
* 免费开源权重
* 无内容审查限制
* 广泛的风格多样性（数字艺术、照片级真实感、动漫等）
* 使用 bfloat16 精度快速处理
* 高质量描述生成
* 内存高效运行
* 在各种图像类型上保持一致性
* 支持多种描述风格
* 针对扩散模型训练优化

模型在多样化数据集上训练，确保：
* 不同图像类型的平衡表示
* 各种场景下的高准确性
* 复杂场景的稳健性能
* 支持 SFW 和 NSFW 内容
* 不同风格和概念的平等覆盖

## 路线图

### ✅ 已完成（v1.3.0）
* ✅ GGUF 模型支持，提供更好的性能
* ✅ 支持 12 种 GGUF 量化格式（Q2_K 到 F16）
* ✅ 增强的错误处理和参数验证
* ✅ 干净的控制台输出（无调试垃圾信息）
* ✅ 改进的内存管理选项
* ✅ 批处理支持（描述工具）
* ✅ CPU 处理性能优化（GGUF CPU 模式）
* ✅ 增强的批处理功能与内存管理

### 🔄 未来计划
* 更多描述风格选项和自定义提示
* 高级微调支持自定义模型
* 实时处理优化
* 多语言描述支持
* 集成更多视觉-语言模型

## 致谢

* **原始 JoyCaption 模型**: [fancyfeast](https://huggingface.co/fancyfeast) - 基础 JoyCaption 模型的创建者
* **GGUF 量化模型**: [mradermacher](https://huggingface.co/mradermacher) - 提供全面的 GGUF 量化模型 (Q2_K 到 F16)
* **备选 GGUF 模型**: [concedo](https://huggingface.co/concedo) - 提供带视觉投影的备选 GGUF 模型
* **ComfyUI 集成**: [1038lab](https://github.com/1038lab) - 此 ComfyUI 自定义节点的开发者
* **LLaVA 框架**: Microsoft Research - 基础视觉-语言模型架构
* **llama-cpp-python**: [abetlen](https://github.com/abetlen/llama-cpp-python) - llama.cpp 的 Python 绑定

## 许可证

本仓库代码基于 GPL-3.0 许可证发布。


模型采用 GPL-3.0 许可证发布。请参阅 [LICENSE](LICENSE) 文件了解详情。 

