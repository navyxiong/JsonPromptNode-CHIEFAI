[README.md](https://github.com/user-attachments/files/24998005/README.md)
# 🎯 高级 JSON 提示词加载器 (Advanced JSON Prompt Loader)

<div align="center">

[![ComfyUI](https://img.shields.io/badge/ComfyUI-Custom%20Node-blue.svg)](https://github.com/comfyanonymous/ComfyUI)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)

一个用于 **ComfyUI** 的高阶提示词管理节点，支持结构化 JSON 预设、智能缓存控制与多源组合。

[<img src="https://img.shields.io/badge/Download-Latest%20Release-blue?style=for-the-badge">](https://github.com/yourusername/json-prompt-node/releases)
[<img src="https://img.shields.io/badge/使用教程-文档-green?style=for-the-badge">](#使用方法)

</div>

---

## 📋 功能特性

- 📁 **本地化预设管理** —— 预设文件存储在节点安装目录，不污染 ComfyUI 全局 `input` 文件夹
- 🔍 **可搜索下拉菜单** —— 内置前端搜索功能，快速定位海量预设文件
- 🔄 **智能缓存控制** —— 支持强制刷新缓存，实时响应外部文件修改（无需重启）
- 📝 **多源提示词组合** —— 默认提示词 + 3类 JSON 预设 + 自定义文本灵活拼接
- 🗂️ **科学分类管理** —— 透视图 / 鸟瞰图 / 其他，三维分类体系
- 🌏 **原生中文支持** —— 完全中文化的参数界面，支持中文 JSON 内容

---

## 📦 安装

### 方法一：Git 克隆（推荐）

```bash
# 进入 ComfyUI 自定义节点目录
cd ComfyUI/custom_nodes

# 克隆仓库
git clone https://github.com/yourusername/json-prompt-node.git

# 重启 ComfyUI，节点将自动初始化目录结构
```

### 方法二：手动安装

1. 下载本仓库 `Code` → `Download ZIP`
2. 解压至 `ComfyUI/custom_nodes/json-prompt-node/`
3. 重启 ComfyUI

### 安装验证

重启后，在 ComfyUI 右键菜单中查找：
```
utils/prompt_loaders → 高级 JSON 提示词加载器 (缓存释放版)
```

节点首次加载时会自动创建以下目录结构：

```
json-prompt-node/
├── __init__.py              # 节点入口
├── json_prompt_node.py      # 主逻辑
├── README.md                # 本文件
└── preset/                  # 预设文件夹（自动生成）
    ├── perspective/         # 透视图预设 (*.json)
    ├── birdview/            # 鸟瞰图预设 (*.json)
    └── others/              # 其他预设 (*.json)
```

---

## 🚀 使用方法

### 1. 准备 JSON 预设文件

将 `.json` 文件放入对应分类文件夹：

| 文件夹路径 | 用途 | 示例文件名 |
|-----------|------|-----------|
| `preset/perspective/` | 透视图/人视角提示词 | `architectural.json`, `street_view.json` |
| `preset/birdview/` | 鸟瞰图/航拍提示词 | `aerial_city.json`, `master_plan.json` |
| `preset/others/` | 其他补充提示词 | `lighting.json`, `quality_tags.json` |

### 2. JSON 格式规范

支持三种格式，节点会自动解析并转换为逗号分隔字符串：

**格式 A：数组（推荐）**
```json
[
    "architectural photography",
    "clean lines", 
    "modern glass facade",
    "symmetrical composition"
]
```

**格式 B：字典（键值对）**
```json
{
    "style": "photorealistic",
    "quality": "8k resolution",
    "lighting": "golden hour",
    "camera": "Sony A7R IV"
}
```

**格式 C：纯字符串**
```json
"architectural photography, clean lines, modern design"
```

> **编码要求**：文件必须使用 **UTF-8** 编码保存，以支持中文内容。

---

## ⚙️ 节点参数说明

### 核心参数

| 参数 | 类型 | 默认值 | 功能描述 |
|------|------|--------|----------|
| `custom_text` | 多行文本 | `""` | 自定义提示词，追加至最终输出末尾 |
| `enable_default_prompt` | 布尔开关 | `True` | 启用通用基础提示词前缀 |
| `透视图` | 下拉选择 | `"None"` | 选择 `preset/perspective/` 下的预设 |
| `鸟瞰图` | 下拉选择 | `"None"` | 选择 `preset/birdview/` 下的预设 |
| `其他` | 下拉选择 | `"None"` | 选择 `preset/others/` 下的预设 |
| `释放缓存` | 布尔按钮 | `False` | 强制刷新，重新读取磁盘上的 JSON 文件 |

### 默认提示词内容

当 `enable_default_prompt` 启用时，自动添加的前缀：

```
Transform the image into a real-life photo according to the following requirements, 
strictly maintain the consistency of the image content, strictly maintain the 
consistency of the buildings and environment in the image, and do not change 
the shooting angle and composition of the image.
```

---

## 🔄 输出逻辑

### 组合顺序（优先级从高到低）

1. **默认提示词**（`enable_default_prompt` = `True` 时）
2. **透视图预设**（选择了非 `"None"` 的文件时）
3. **鸟瞰图预设**（选择了非 `"None"` 的文件时）
4. **其他预设**（选择了非 `"None"` 的文件时）
5. **自定义文本**（`custom_text` 非空时）

### 拼接规则

- **连接符**：`, `（英文逗号 + 空格）
- **空值过滤**：自动跳过 `"None"`、空字符串、仅含空白字符的项
- **原始保留**：不进行自动去重，允许内容重复（保持用户控制）

### 核心算法

```python
def generate_final_prompt(parts):
    """
    parts: [default_prompt, perspective, birdview, others, custom_text]
    """
    # 清洗与过滤空值
    filtered = [
        part.strip() 
        for part in parts 
        if part and part.strip() and part != "None"
    ]

    # 使用 ", " 连接所有有效部分
    return ", ".join(filtered)
```

### 输出示例

**输入配置：**
- `enable_default_prompt`: `True`
- `透视图`: `architectural.json`（内容：`["modern building", "glass facade"]`）
- `鸟瞰图`: `"None"`
- `其他`: `quality.json`（内容：`["masterpiece", "8k"]`）
- `custom_text`: `sunset lighting, golden hour`

**最终输出：**
```
Transform the image into a real-life photo according to the following requirements..., modern building, glass facade, masterpiece, 8k, sunset lighting, golden hour
```

---

## 💡 使用示例

### 示例 1：建筑透视表现

**文件**: `preset/perspective/architectural.json`
```json
["architectural photography", "modernist", "glass curtain wall", "symmetrical"]
```

**节点参数**:
- `enable_default_prompt`: ✅ 启用
- `透视图`: `architectural.json`
- `其他`: `quality.json` (内容为 `["8k", "masterpiece"]`)
- `custom_text`: `sunset lighting, warm tone`

**最终输出**：
```
Transform the image into a real-life photo according to the following requirements..., architectural photography, modernist, glass curtain wall, symmetrical, 8k, masterpiece, sunset lighting, warm tone
```

### 示例 2：仅使用自定义（轻量模式）

**节点参数**:
- `enable_default_prompt`: ❌ 禁用
- `透视图`: `"None"`
- `鸟瞰图`: `"None"`
- `其他`: `"None"`
- `custom_text`: `beautiful mountain landscape, foggy morning, cinematic`

**最终输出**：
```
beautiful mountain landscape, foggy morning, cinematic
```

### 示例 3：字典格式解析

**文件**: `preset/others/camera_settings.json`
```json
{
    "camera": "DSLR",
    "lens": "35mm",
    "aperture": "f/1.8"
}
```

**节点参数**:
- `其他`: `camera_settings.json`
- 其余: 默认

**解析结果**：
```
DSLR, 35mm, f/1.8
```

---

## 🛠️ 故障排除

| 问题现象 | 可能原因 | 解决方案 |
|---------|---------|---------|
| **下拉菜单为空** | 未在对应文件夹放置 `.json` 文件 | 检查文件是否放入正确的 `preset/` 子文件夹 |
| **修改 JSON 后不生效** | ComfyUI 缓存了旧版本 | 勾选 `释放缓存` 并重新执行，或重启 ComfyUI |
| **中文内容乱码** | JSON 文件编码非 UTF-8 | 用 VS Code/Notepad++ 将文件转为 UTF-8 编码保存 |
| **文件找不到** | JSON 文件放错分类文件夹 | 确认文件在 `perspective/`、`birdview/` 或 `others/` 内 |
| **提示词未按预期组合** | 某预设选择了 `"None"` | 检查下拉菜单是否确实选中了目标文件 |

---

## 📝 更新日志

### v1.0.0 (2025-XX-XX)
- ✨ 初始版本发布
- 📁 支持从节点目录 `preset` 文件夹读取 JSON 预设
- 🔍 支持前端搜索功能
- 🔄 支持缓存强制刷新
- 🌏 完整中文界面支持

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目基于 [MIT](LICENSE) 许可证开源。

---

## 🙏 致谢

- 感谢 [ComfyUI](https://github.com/comfyanonymous/ComfyUI) 团队提供优秀的节点式生图平台
- 感谢社区用户的反馈与建议

<div align="center">

**⭐ 如果此节点对您有帮助，请点个 Star 支持一下！**

</div>
