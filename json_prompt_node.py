import os
import json
import folder_paths

PRESET_FOLDERS = {
    "透视图": "perspective",
    "鸟瞰图": "birdview",
    "其他": "others"
}

class JsonPromptNode:
    @classmethod
    def INPUT_TYPES(s):
        # 实时计算路径
        base_dir = os.path.dirname(os.path.abspath(__file__))
        preset_root = os.path.join(base_dir, "preset")
        optional_inputs = {}

        for preset_name, sub_folder in PRESET_FOLDERS.items():
            target_dir = os.path.join(preset_root, sub_folder)
            os.makedirs(target_dir, exist_ok=True)
            files = ["None"] + sorted([f for f in os.listdir(target_dir) if f.endswith(".json")])
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
    FUNCTION = "process_prompts"
    CATEGORY = "Archi-Prompt/Loaders"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # 强制 ComfyUI 检查：只要点击了运行或者文件选择变了，就生成新的指纹
        return float("nan") if kwargs.get("refresh_cache") else str(kwargs)

    def process_prompts(self, custom_text, enable_default_prompt, refresh_cache, **kwargs):
        parts = []
        if enable_default_prompt:
            parts.append("Transform the image into a real-life photo...")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        for preset_name, sub_folder in PRESET_FOLDERS.items():
            filename = kwargs.get(preset_name, "None")
            if filename and filename != "None":
                file_path = os.path.join(base_dir, "preset", sub_folder, filename)
                
                if os.path.exists(file_path):
                    try:
                        # 核心修复：尝试多种编码读取，防止中文乱码导致失败
                        content = ""
                        for encoding in ['utf-8-sig', 'utf-8', 'gbk']:
                            try:
                                with open(file_path, 'r', encoding=encoding) as f:
                                    data = json.load(f)
                                    if isinstance(data, list): content = ", ".join(map(str, data))
                                    elif isinstance(data, dict): content = ", ".join(map(str, data.values()))
                                    else: content = str(data)
                                break 
                            except: continue
                        
                        if content: parts.append(content)
                    except Exception as e:
                        print(f"!!! [Archi-Prompt] Read Error: {e}")

        if custom_text.strip(): parts.append(custom_text.strip())
        
        result = ", ".join([p.strip() for p in parts if p.strip()])
        print(f"\n>>> [Final Output]: {result[:50]}...") # 在控制台打印前50个字符确认
        return (result,)
