from .json_prompt_node import JsonPromptNode

NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "Advanced JSON Prompt Loader"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
