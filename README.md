# ComfyUI Advanced JSON Prompt Loader (Multi)

**Advanced JSON Prompt Loader (Multi)** 是一个功能强大的 ComfyUI 自定义节点，专为复杂的提示词（Prompt）管理设计。

它允许你通过 **3 个独立插槽** 同时加载不同的 JSON 预设文件（如风格、光影、角色），并与**内置默认提示词**及**临时自定义文本**智能合并，像搭积木一样构建最终的提示词。

---

## ✨ 核心功能 (Features)

* **🧩 多路混合加载**：提供 3 个独立的预设插槽 (`preset_1`, `preset_2`, `preset_3`)，可同时读取并合并 3 个不同的 JSON 文件。
* **📂 自动目录管理**：无需手动创建文件夹，节点首次运行时会自动在 `ComfyUI/input/` 下创建 `prompt_presets` 目录。
* **⬇️ 下拉菜单选择**：自动扫描目录下的 JSON 文件，通过下拉菜单直接选择，支持热插拔。
* **🚫 灵活停用**：每个插槽均提供 `"None"` 选项，不需要的插槽选为 None 即可跳过。
* **⚡ 默认起手式开关**：内置高质量通用提示词（Masterpiece, Best Quality...），可通过 `enable_default_prompt` 开关一键启用/禁用。
* **📝 临时自定义输入**：提供多行文本框，用于输入本次生成特有的描述。

---

## 📦 安装方法 (Installation)

### 方法 1: 手动安装 (推荐)
1.  在你的 `ComfyUI/custom_nodes/` 目录下创建一个新文件夹，例如命名为 `ComfyUI-JSON-Prompt-Multi`。
2.  将 `__init__.py` 和 `json_prompt_node.py` (以及本 README) 放入该文件夹中。
3.  重启 ComfyUI。

### 方法 2: Git Clone
如果有 Git 环境，在 `ComfyUI/custom_nodes/` 目录下运行：
```bash
git clone [https://github.com/navyxiong/ComfyUI-JSON-Prompt-Multi.git](https://github.com/navyxiong/ComfyUI-JSON-Prompt-Multi.git)。

---

## 📂 文件存放路径 (Directory Structure)

首次运行节点并重启 ComfyUI 后，系统会自动创建以下目录结构。请将你的 .json 提示词文件放入 prompt_presets 文件夹中。
ComfyUI
├── custom_nodes
│   └── ComfyUI-JSON-Prompt-Multi
│       ├── __init__.py
│       └── json_prompt_node.py
└── input
    └── prompt_presets  <-- 【在此处放入你的JSON文件】
        ├── style_cyberpunk.json
        ├── lighting_cinematic.json
        └── character_robot.json

---

## 🚀 使用指南 (Usage)
加载节点：

双击画布搜索 Advanced JSON Prompt Loader (Multi)。

或在菜单 utils -> prompt_loaders 中找到。

配置参数：

custom_text: 输入临时的提示词（例如：1girl, sitting on a bench）。

enable_default_prompt: 是否在最前方添加内置的起手式提示词。

preset_1 / 2 / 3: 下拉选择你要混合的 JSON 文件。如果只想用 1 个文件，将其他两个选为 None。

连接输出：

将节点的 final_prompt 输出端连接到 CLIP Text Encode (Prompt) 节点的文本输入端。

注意：你可能需要右键点击 CLIP Text Encode 节点，选择 "Convert text to input" 才能看到连接点。
