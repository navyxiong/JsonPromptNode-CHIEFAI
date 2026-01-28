# ComfyUI Advanced JSON Prompt Loader

一个功能强大的 ComfyUI 自定义节点，旨在优化提示词（Prompt）的管理流程。它允许你将“内嵌默认提示词”、“外部 JSON 预设文件”和“临时自定义文本”三者智能合并，并输出为最终的提示词字符串。

![Node Screenshot](https://via.placeholder.com/800x200?text=Node+Screenshot+Placeholder)
*(此处可放一张节点运行截图)*

## ✨ 主要功能 (Features)

* **📂 自动目录管理**：无需手动创建文件夹，节点首次运行时会自动在 `ComfyUI/input/` 下创建 `prompt_presets` 目录。
* **⬇️ 下拉菜单选择**：自动扫描 `prompt_presets` 目录下的 JSON 文件，通过下拉菜单直接选择，告别手动输入路径的繁琐与易错。
* **🔌 默认提示词开关**：内置通用的高质量起手式提示词（Quality Tags），可通过 Toggle 开关一键启用或禁用。
* **📝 灵活的自定义输入**：提供多行文本框，方便临时补充或调整提示词。
* **🔗 智能合并**：自动处理分隔符，将三个来源的提示词无缝拼接。

## 📦 安装方法 (Installation)

### 方法 1: 手动安装
1.  下载本项目的所有文件。
2.  将整个文件夹放入你的 ComfyUI `custom_nodes` 目录下，例如：
    `ComfyUI/custom_nodes/ComfyUI-JSON-Prompt-Loader`
3.  重启 ComfyUI。

### 方法 2: Git Clone
在 `ComfyUI/custom_nodes/` 目录下打开终端/CMD，运行：
```bash
git clone [https://github.com/YourUsername/ComfyUI-JSON-Prompt-Loader.git](https://github.com/YourUsername/ComfyUI-JSON-Prompt-Loader.git)

## 🚀 使用指南 (Usage)
1. 准备 JSON 预设文件
首次重启 ComfyUI 后，插件会自动创建以下目录：
ComfyUI
└── input
    └── prompt_presets  <-- 自动创建的文件夹
请将你的 .json 提示词文件（例如 styles.json, characters.json）放入该文件夹中。

2. 添加节点
在 ComfyUI 画布中双击，搜索 "Advanced JSON Prompt Loader"。

或者在分类菜单 utils -> prompt_loaders 中找到它。

3. 参数说明
json_filename: 点击下拉菜单，选择你刚刚放入 prompt_presets 文件夹中的 JSON 文件。

custom_text: 在此输入任何你想补充的特定描述（例如：1girl, red hair, sitting）。

enable_default_prompt: 开启后，会自动在最前方加入默认的高质量提示词（如 masterpiece, best quality...）。

4. 连接输出
将节点的 final_prompt 输出端连接到 CLIP Text Encode (Prompt) 的文本输入端（需将 CLIP Text Encode 转为 Input 输入模式）。

📄 JSON 文件格式支持
本节点支持两种常见的 JSON 结构，并会自动将其转换为逗号分隔的字符串。

格式 A：字符串列表 (推荐) 适用于纯标签管理。

[
  "photorealistic",
  "8k resolution",
  "cinematic lighting",
  "highly detailed"
]

格式 B：键值对字典 适用于带有分类管理的提示词，节点会提取所有的 Value（值）。
{
  "style": "cyberpunk",
  "camera": "wide angle",
  "lighting": "neon lights"
}

## 🛠️ 常见问题 (FAQ)
Q: 为什么下拉菜单里找不到我的文件？ A: 请确保文件后缀名为 .json，且已放入 ComfyUI/input/prompt_presets 文件夹中。放入文件后，请点击 ComfyUI 菜单面板的 "Refresh" 按钮或刷新网页。

Q: 如果不放 JSON 文件会怎样？ A: 节点会显示一个占位选项，你可以仅使用“默认提示词”和“自定义文本”功能，不会报错。
