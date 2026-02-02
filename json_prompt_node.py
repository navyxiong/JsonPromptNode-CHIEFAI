import os
import json
import time
import folder_paths

# 预设子文件夹映射（键名为前端显示的分类，值名为实际文件夹名）
PRESET_FOLDERS = {
    "透视图": "perspective",
    "鸟瞰图": "birdview",
    "其他": "others"
}

DEFAULT_PROMPT_TEXT = (
    "Transform the image into a real-life photo according to the following requirements, "
    "strictly maintain the consistency of the image content, strictly maintain the consistency "
    "of the buildings and environment in the image, and do not change the shooting angle and "
    "composition of the image."
)

class JsonPromptNode:
    def __init__(self):
        # 自动定位到插件目录下的 preset 文件夹
        self.node_dir = os.path.dirname(os.path.abspath(__file__))
        self.preset_root = os.path.join(self.node_dir, "preset")

    @classmethod
    def INPUT_TYPES(s):
        node_dir = os.path.dirname(os.path.abspath(__file__))
        preset_root = os.path.join(node_dir, "preset")
        optional_inputs = {}

        # 遍历预设文件夹并获取文件列表
        for preset_name, sub_folder in PRESET_FOLDERS.items():
            target_dir = os.path.join(preset_root, sub_folder)
            
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir, exist_ok=True)
                except Exception as e:
                    print(f"[Archi-prompt-preset] Warning: Cannot create {target_dir}: {e}")

            files = ["None"]
            if os.path.exists(target_dir):
                try:
                    json_files = [f for f in os.listdir(target_dir) if f.endswith(".json")]
                    files.extend(sorted(json_files))
                except Exception as e:
                    print(f"[Archi-prompt-preset] Error reading {target_dir}: {e}")

            optional_inputs[preset_name] = (files, {"searchable": True})

        return {
            "required": {
                "custom_text": ("STRING", {"multiline": True, "default": "", "placeholder": "Enter custom prompts here..."}),
                "enable_default_prompt": ("BOOLEAN", {"default": True, "label_on": "Enable Default", "label_off": "Disable Default"}),
                "refresh_cache": ("BOOLEAN", {"default": False, "label_on": "FORCE REFRESH", "label_off": "Normal"}),
            },
            "optional": optional_inputs
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "process_prompts"
    CATEGORY = "Archi-Prompt/Loaders"

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        """
        核心修复：通过哈希追踪所有输入参数的变化，包括动态生成的下拉菜单。
        """
        if kwargs.get("refresh_cache", False):
            return float("nan") # 强制重新运行
        
        # 提取关键变量进行哈希追踪
        custom_text = kwargs.get("custom_text", "")
        enable_default = kwargs.get("enable_default_prompt", True)
        # 追踪下拉菜单选中的文件名
        selections = [kwargs.get(k, "None") for k in PRESET_FOLDERS.keys()]
        
        return hash((custom_text, enable_default, tuple(selections)))

    def load_preset(self, filename, sub_folder):
        if not filename or filename == "None":
            return None
        
        file_path = os.path.join(self.preset_root, sub_folder, filename)
        if not os.path.exists(file_path):
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 兼容数组、字典或纯字符串格式
                if isinstance(data, list):
                    return ", ".join([str(item) for item in data])
                elif isinstance(data, dict):
                    return ", ".join([str(v) for v in data.values()])
                return str(data)
        except Exception as e:
            print(f"[Archi-prompt-preset] Error loading {filename}: {e}")
            return None

    def process_prompts(self, custom_text, enable_default_prompt, refresh_cache, **kwargs):
        parts = []
        
        # 1. 默认提示词
        if enable_default_prompt:
            parts.append(DEFAULT_PROMPT_TEXT)

        # 2. 动态读取选中的 JSON 内容
        for preset_name, sub_folder in PRESET_FOLDERS.items():
            filename = kwargs.get(preset_name, "None")
            content = self.load_preset(filename, sub_folder)
            if content:
                parts.append(content)

        # 3. 自定义文本
        if custom_text and custom_text.strip():
            parts.append(custom_text.strip())

        final_output = ", ".join([p.strip() for p in parts if p and p.strip()])
        return (final_output,)

# 映射给 ComfyUI 使用
NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "Archi-Prompt JSON Loader (Advanced)"
}
