import os
import json
import folder_paths

# 1. 内嵌的默认提示词
DEFAULT_PROMPT_TEXT =
        "Transform the image into a real-life photo according to the following requirements, "
        "strictly maintain the consistency of the image content, strictly maintain the consistency "
        "of the buildings and environment in the image, and do not change the shooting angle and "
        "composition of the image."

# 2. 定义子文件夹名称
SUB_FOLDER_NAME = "prompt_presets"

class JsonPromptNode:
    """
    升级版：支持同时加载多个 JSON 预设文件。
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # --- 获取文件列表逻辑 ---
        input_root = folder_paths.get_input_directory()
        target_dir = os.path.join(input_root, SUB_FOLDER_NAME)

        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir, exist_ok=True)
            except:
                pass

        files = []
        if os.path.exists(target_dir):
            files = [f for f in os.listdir(target_dir) if f.endswith(".json")]
        
        # --- 关键修改：添加 "None" 选项 ---
        # 这样用户可以选择不加载某个插槽
        file_options = ["None"] + sorted(files)

        return {
            "required": {
                # 自定义文本放在最上面，方便输入
                "custom_text": ("STRING", {"multiline": True, "default": "", "placeholder": "在此输入自定义提示词..."}),
                "enable_default_prompt": ("BOOLEAN", {"default": True, "label_on": "Enable Default", "label_off": "Disable Default"}),
            },
            "optional": {
                # --- 关键修改：提供3个预设插槽 ---
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

        # 2. 定义一个内部函数来加载单个文件
        def load_preset(filename):
            if filename == "None":
                return None
            
            file_path = os.path.join(input_root, SUB_FOLDER_NAME, filename)
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            return ", ".join([str(item) for item in data])
                        elif isinstance(data, dict):
                            return ", ".join([str(v) for v in data.values()])
                        else:
                            return str(data)
                except Exception as e:
                    print(f"[JsonPromptNode] Error loading {filename}: {e}")
            return None

        # 3. 依次处理三个插槽
        for preset in [preset_1, preset_2, preset_3]:
            content = load_preset(preset)
            if content:
                parts.append(content)

        # 4. 自定义文本
        if custom_text and custom_text.strip() != "":
            parts.append(custom_text)

        # 5. 合并
        final_output = ", ".join([p.strip() for p in parts if p.strip()])
        
        return (final_output,)

# 映射
NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "Advanced JSON Prompt Loader (Multi)"
}
