# ComfyUI 便携版 `llama-cpp-python` CUDA 安装指南

本指南帮助您为 ComfyUI 的 Windows 便携版安装支持 GPU (CUDA) 的 `llama-cpp-python`。

---

### **1. 打开 ComfyUI 的命令提示符**

* 进入 `C:\ComfyUI_windows_portable\python_embeded`
* 在地址栏中输入 `cmd` 并按回车键。

---

### **2. 安装构建工具（如果尚未安装）**

* **安装 Visual Studio Build Tools：**
    * 从 [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/) 下载（在"Tools for Visual Studio"下）。
    * 运行安装程序，选择 **"Desktop development with C++"** 工作负载。
* **安装 NVIDIA CUDA Toolkit：**
    * 从 [https://developer.nvidia.com/cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive) 下载您的 CUDA 版本（例如 12.6）。
    * 运行安装程序，确保选中 **"Visual Studio Integration"**。

## **自动安装脚本（推荐）**

* 确保安装脚本保存在这里：  
  `.\ComfyUI\custom_nodes\ComfyUI-JoyCaption\llama_cpp_install\llama_cpp_install.py`

* 在命令提示符中（在步骤 1 中打开的），运行脚本：

  ```bash
  .\python_embeded\python.exe llama_cpp_install.py
  ```

脚本将执行以下操作：

* 升级 pip
* 清除 pip 缓存
* 安装最小构建依赖项（scikit-build-core, cmake）
* 检测 GPU 并在可用时构建支持 CUDA 的 llama-cpp-python

🕒 此过程可能需要 5-20+ 分钟，具体取决于您的系统。

### **重启 ComfyUI**

* 关闭 ComfyUI。
* 重启 ComfyUI。
* 使用 Ctrl+F5（Windows）或 Cmd+Shift+R（macOS）硬刷新浏览器。

## **手动安装**
---

### **1. 准备 Python 环境**

* 在命令提示符中运行：
    ```bash
    .\python.exe -m pip install --upgrade pip
    .\python.exe -m pip cache purge
    .\python.exe -m pip install scikit-build-core cmake
    ```

---

### **2. 编译并安装 `llama-cpp-python`**

* 在命令提示符中运行：
    ```bash
    set CMAKE_ARGS="-DGGML_CUDA=on" && .\python.exe -m pip install llama-cpp-python --no-cache-dir && set CMAKE_ARGS=
    ```
    * **耐心等待。** 这需要时间（5-20+ 分钟）。

---

### **3. 重启 ComfyUI**

* 关闭 ComfyUI。
* 重启 ComfyUI。
* 硬刷新网页浏览器（`Ctrl+F5` 或 `Cmd+Shift+R`）。

--- 