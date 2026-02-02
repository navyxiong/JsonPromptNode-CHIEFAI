# Archi-Prompt JSON Loader for ComfyUI
Archi-Prompt JSON Loader 是一个专为建筑可视化工作流设计的 ComfyUI 自定义节点。它允许用户通过下拉菜单动态加载本地的 JSON 预设文件，并将其解析为结构化的提示词（Prompt）。

该节点特别适合管理复杂的建筑风格、光照、材质等提示词库，支持“透视图”和“鸟瞰图”分类管理。

## ✨ 功能特点
动态加载预设：无需重启 ComfyUI，即可读取 preset 文件夹下的 JSON 文件。

结构化解析：自动解析 JSON 中的 values 或 list 内容，并拼接成字符串。

多编码支持：兼容 utf-8, utf-8-sig, gbk 编码，完美支持中文 JSON 文件。

内置通用起手式：提供 enable_default_prompt 开关，自动添加 "Transform the image into a real-life photo..." 等控制画风的一致性提示词。

双语界面：节点输入项使用中文标签（透视图/鸟瞰图），文件夹使用英文命名，便于管理。

## 📂 安装与目录结构
进入您的 ComfyUI 插件目录：cd ComfyUI/custom_nodes/

新建文件夹（例如 ComfyUI-Archi-Prompt）并将 json_prompt_node.py 放入其中。

关键步骤：在节点同级目录下创建以下文件夹结构，并放入您的 JSON 文件：

<img width="698" height="310" alt="image" src="https://github.com/user-attachments/assets/35244a24-a3dc-4731-9b9f-6c40834e5852" />


## 📝 使用说明
在 ComfyUI 中搜索节点名称：Archi-Prompt JSON Loader

输入参数 (Inputs) 

<img width="706" height="242" alt="image" src="https://github.com/user-attachments/assets/1c11c3e1-d56e-4faf-9e2a-78304cfece18" />


## 📄 JSON 文件格式规范
该节点支持两种 JSON 格式。您之前生成的风格反推提示词可以直接保存使用。

格式 A：字典 (推荐)
节点将自动提取所有的 value 并用逗号拼接。key 仅作注释用，不会被输出。
{
  "camera": "High-angle drone shot, 45° Bird's eye",
  "lighting": "Golden hour, Soft diffuse light",
  "engine": "Unreal Engine 5, 8k resolution"
}
输出结果： High-angle drone shot, 45° Bird's eye, Golden hour, Soft diffuse light, Unreal Engine 5, 8k resolution

格式 B：列表
直接读取列表中的所有字符串。
[
  "Cinematic Aerial Shot",
  "Wide-angle 24mm",
  "Magic Hour"
]
输出结果： Cinematic Aerial Shot, Wide-angle 24mm, Magic Hour

## 🛠️ 常见问题
下拉菜单里是空的？

请检查 preset/birdview 或 preset/perspective 文件夹是否已创建。

文件夹内是否有 .json 后缀的文件。

点击一次 Queue Prompt 运行（或切换 refresh_cache）来触发刷新。

JSON 读取报错？

请确保 JSON 语法正确（可以使用在线 JSON 校验工具）。

节点已内置多种编码处理，通常不会出现乱码问题。
