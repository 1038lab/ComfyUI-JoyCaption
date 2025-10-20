# `llama-cpp-python` CUDA Installation for ComfyUI Portable

This guide helps you install `llama-cpp-python` with GPU (CUDA) support for ComfyUI's Windows portable version.

---

### **1. Open ComfyUI's Command Prompt**

* Go to `C:\ComfyUI_windows_portable\python_embeded`
* In the address bar, type `cmd` and press Enter.

---

### **2. Install Build Tools (If you haven't already)**

* **Install Visual Studio Build Tools:**
    * Download from [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/) (under "Tools for Visual Studio").
    * Run installer, select **"Desktop development with C++"** workload.
* **Install NVIDIA CUDA Toolkit:**
    * Download your CUDA version (e.g., 12.6) from [https://developer.nvidia.com/cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive).
    * Run installer, ensure **"Visual Studio Integration"** is selected.

## **Automatic Installation Script (Recommended)**

* Make sure the installation script is saved here:  
  `.\ComfyUI\custom_nodes\ComfyUI-JoyCaption\install_llama_official.py`

* In the command prompt (opened in step 1), run the script with:

  ```bash
  .\python_embeded\python.exe llama_cpp_install.py
  ```

The script will:

* Upgrade pip
* Clear pip cache
* Install minimal build dependencies (scikit-build-core, cmake)
* Detect GPU and build llama-cpp-python with CUDA support if available

🕒 This process may take 5–20+ minutes depending on your system.

### ** Restart ComfyUI**

* Close ComfyUI.
* Restart ComfyUI.
* Hard refresh your browser with Ctrl+F5 (Windows) or Cmd+Shift+R (macOS).




## **Manuelly Installation**
---

### **1. Prepare Python Environment**

* In the command prompt, run:
    ```bash
    .\python.exe -m pip install --upgrade pip
    .\python.exe -m pip cache purge
    .\python.exe -m pip install scikit-build-core cmake
    ```

---

### **2. Compile and Install `llama-cpp-python`**

* In the command prompt, run:
    ```bash
    set CMAKE_ARGS="-DGGML_CUDA=on" && .\python.exe -m pip install llama-cpp-python --no-cache-dir && set CMAKE_ARGS=
    ```
    * **Wait patiently.** This takes time (5-20+ minutes).

---

### **3. Restart ComfyUI**

* Close ComfyUI.
* Restart ComfyUI.
* Hard refresh your web browser (`Ctrl+F5` or `Cmd+Shift+R`).

---

