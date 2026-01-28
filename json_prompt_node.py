import os
import json
import folder_paths

# 修复：使用括号包裹多行字符串，确保 Python 语法正确
DEFAULT_PROMPT_TEXT = (
    "Transform the image into a real-life photo according to the following requirements, "
    "strictly maintain the consistency of the image content, strictly maintain the consistency "
    "of the buildings and environment in the image, and do not change the shooting angle and "
    "composition of the image."
)

SUB_FOLDER_NAME = "prompt_presets"

class JsonPromptNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        input_root = folder_paths.get_input_directory()
        target_dir = os.path.join(input_root, SUB_FOLDER_NAME)

        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir, exist_ok=True)
            except Exception as e:
                print(f"[JsonPromptNode] Warning: Could not create directory {target_dir}: {e}")

        files = []
        if os.path.exists(target_dir):
            files = [f for f in os.listdir(target_dir) if f.endswith(".json")]
        
        file_options = ["None"] + sorted(files)

        return {
            "required": {
                "custom_text": ("STRING", {"multiline": True, "default": "", "placeholder": "在此输入自定义提示词..."}),
                "enable_default_prompt": ("BOOLEAN", {"default": True, "label_on": "Enable Default", "label_off": "Disable Default"}),
            },
            "optional": {
                "preset_1": (file_options, ),
                "preset_2": (file_options, ),
                "preset_3": (file_options, ),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "process_prompts"
    CATEGORY = "utils/prompt_loaders"

    def process_prompts(self, custom_text, enable_default_prompt, preset_1="None", preset_2="None", preset_3="None"):
        parts = []
        input_root = folder_paths.get_input_directory()
        
        # 1. 默认提示词
        if enable_default_prompt:
            parts.append(DEFAULT_PROMPT_TEXT)

        # 2. 内部加载函数
        def load_preset(filename):
            if not filename or filename == "None":
                return None
            
            file_path = os.path.join(input_root, SUB_FOLDER_NAME, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            return ", ".join([str(item) for item in data])
                        elif isinstance(data, dict):
                            # 针对你常用的建筑摄影 JSON 结构，提取所有值
                            return ", ".join([str(v) for v in data.values()])
                        else:
                            return str(data)
                except Exception as e:
                    print(f"[JsonPromptNode] Error loading {filename}: {e}")
            return None

        # 3. 处理插槽
        for preset in [preset_1, preset_2, preset_3]:
            content = load_preset(preset)
            if content:
                parts.append(content)

        # 4. 自定义文本
        if custom_text and custom_text.strip():
            parts.append(custom_text)

        # 5. 合并并去重/清理多余逗号
        final_output = ", ".join([p.strip() for p in parts if p.strip()])
        
        return (final_output,)

NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "Advanced JSON Prompt Loader (Multi)"
}
