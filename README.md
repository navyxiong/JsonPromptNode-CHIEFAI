# Archi-Prompt JSON Loader for ComfyUI
一个专为建筑摄影和渲染设计的 ComfyUI 自定义节点，允许用户通过结构化的 JSON 文件 快速加载和组合提示词。

核心功能
多维度组合：支持同时从“透视图”和“鸟瞰图”预设库中选择配置。

固定提示词优化：内置一键开启的高质量建筑实景化基础提示词。

实时刷新：通过 refresh_cache 开关快速同步本地新增的 JSON 文件。

多格式兼容：支持 JSON 列表 (List) 或 字典 (Dict) 格式，自动处理多种字符编码。

## 目录结构

为了让节点识别您的预设，请确保您的插件目录结构如下：

<img width="676" height="172" alt="image" src="https://github.com/user-attachments/assets/e1e0d43f-5e93-43e5-a881-3a6a16281938" />

## 使用指南

### 节点参数

custom_text: 手动输入的补充提示词。

enable_default_prompt: 是否启用内置的建筑写实增强引导语。

refresh_cache: 设为 True 时，ComfyUI 将强制刷新文件列表。

透视图 / 鸟瞰图: 下拉菜单选择对应的 .json 文件。

### JSON 文件示例

您可以使用以下两种格式之一：

<img width="682" height="189" alt="image" src="https://github.com/user-attachments/assets/34bb2a87-41d1-4e85-8e19-08b382d3189a" />

## 安装方法
进入您的 ComfyUI custom_nodes 目录。

创建一个文件夹（例如 Archi-Prompt）。

将 json_prompt_node.py 放入该文件夹。

手动创建 preset/perspective 和 preset/birdview 文件夹并放入您的 JSON 预设。

重启 ComfyUI。
