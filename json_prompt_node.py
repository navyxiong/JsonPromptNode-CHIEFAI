import os
import json

# 1. 修改：去掉了 "其他": "others"
PRESET_FOLDERS = {
    "透视图": "perspective",
    "鸟瞰图": "birdview"
}

class JsonPromptNode:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def INPUT_TYPES(s):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        preset_root = os.path.join(base_dir, "preset")
        optional_inputs = {}

        for preset_name, sub_folder in PRESET_FOLDERS.items():
            target_dir = os.path.join(preset_root, sub_folder)
            
            # 2. 修改：移除了 os.makedirs(target_dir, exist_ok=True)
            # 新增逻辑：检查目录是否存在。如果不存在（用户未手动创建），则列表仅为 None，防止报错。
            if os.path.exists(target_dir):
                files = ["None"] + sorted([f for f in os.listdir(target_dir) if f.endswith(".json")])
            else:
                files = ["None"]
                
            optional_inputs[preset_name] = (files, {"searchable": True})

        return {
            "required": {
                "custom_text": ("STRING", {"multiline": True, "default": ""}),
                "enable_default_prompt": ("BOOLEAN", {"default": True}),
                "refresh_cache": ("BOOLEAN", {"default": False}),
            },
            "optional": optional_inputs
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "process_prompts"
    CATEGORY = "Archi-Prompt/Loaders"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 只要点击运行或参数变动，立即刷新指纹
        if kwargs.get("refresh_cache", False):
            return float("nan")
        return str(kwargs)

    def process_prompts(self, custom_text, enable_default_prompt, refresh_cache, **kwargs):
        parts = []
        # 固定提示词逻辑
        if enable_default_prompt:
            parts.append( "Transform the image into a real-life photo according to the following requirements, "
                          "strictly maintain the consistency of the image content, strictly maintain the consistency "
                          "of the buildings and environment in the image, and do not change the shooting angle and "
                          "composition of the image.")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        for preset_name, sub_folder in PRESET_FOLDERS.items():
            filename = kwargs.get(preset_name, "None")
            if filename and filename != "None":
                file_path = os.path.join(base_dir, "preset", sub_folder, filename)
                
                if os.path.exists(file_path):
                    # 支持多种编码读取
                    for encoding in ['utf-8-sig', 'utf-8', 'gbk']:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                data = json.load(f)
                                # 兼容 list 或 dict 格式的 JSON
                                content = ", ".join(map(str, data)) if isinstance(data, list) else (", ".join(map(str, data.values())) if isinstance(data, dict) else str(data))
                                if content: parts.append(content)
                            break 
                        except: continue

        if custom_text.strip():
            parts.append(custom_text.strip())

        return (", ".join([p.strip() for p in parts if p.strip()]),)

# 节点映射
NODE_CLASS_MAPPINGS = { "JsonPromptNode": JsonPromptNode }
NODE_DISPLAY_NAME_MAPPINGS = { "JsonPromptNode": "Archi-Prompt JSON Loader" }
