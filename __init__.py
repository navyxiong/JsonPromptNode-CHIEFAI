from .json_prompt_node import JsonPromptNode

# 节点类映射：ComfyUI 核心通过此字典查找你的类
NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

# 节点显示名称映射：这是你在 ComfyUI 界面上看到的节点标题
NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "Advanced JSON Prompt Loader (Multi)"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
