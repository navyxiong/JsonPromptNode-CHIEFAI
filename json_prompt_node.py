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
    一个用于加载默认提示词、外部JSON文件和自定义文本的ComfyUI节点。
    会自动在 input 目录下寻找/创建 'prompt_presets' 文件夹，并读取其中的 JSON 文件。
    """
    
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        # 获取 ComfyUI 的标准 input 目录路径
        input_root = folder_paths.get_input_directory()
        
        # 拼接目标路径: ComfyUI/input/prompt_presets
        target_dir = os.path.join(input_root, SUB_FOLDER_NAME)

        # 核心逻辑：如果文件夹不存在，自动创建它
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir, exist_ok=True)
                print(f"[JsonPromptNode] Created folder: {target_dir}")
            except Exception as e:
                print(f"[JsonPromptNode] Failed to create folder: {e}")

        # 扫描该子目录下的 .json 文件
        files = []
        if os.path.exists(target_dir):
            files = [f for f in os.listdir(target_dir) if f.endswith(".json")]
        
        # 如果没有找到文件，给一个占位符，提示用户
        if not files:
            files = [f"put_files_in_{SUB_FOLDER_NAME}_folder.json"]

        return {
            "required": {
                # 1. JSON文件选择 (下拉菜单形式，读取 prompt_presets 子目录)
                "json_filename": (sorted(files), ),

                # 2. 自定义输入框 (多行文本)
                "custom_text": ("STRING", {"multiline": True, "default": "", "placeholder": "在此输入自定义提示词..."}),
                
                # 3. 开关：是否启用内嵌默认提示词
                "enable_default_prompt": ("BOOLEAN", {"default": True, "label_on": "Enable Default", "label_off": "Disable Default"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "process_prompts"
    CATEGORY = "utils/prompt_loaders"

    def process_prompts(self, custom_text, enable_default_prompt, json_filename):
        parts = []
        
        # --- 1. 处理默认提示词 ---
        if enable_default_prompt:
            parts.append(DEFAULT_PROMPT_TEXT)

        # --- 2. 处理 JSON 文件加载 ---
        input_root = folder_paths.get_input_directory()
        # 拼接完整的子目录路径
        target_file_path = os.path.join(input_root, SUB_FOLDER_NAME, json_filename)

        # 检查文件是否存在且不是占位符
        if os.path.exists(target_file_path) and json_filename.endswith(".json"):
            try:
                with open(target_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 智能解析逻辑
                    if isinstance(data, list):
                        # 列表转字符串
                        parts.append(", ".join([str(item) for item in data]))
                    elif isinstance(data, dict):
                        # 字典转字符串
                        parts.append(", ".join([str(v) for v in data.values()]))
                    else:
                        parts.append(str(data))
                        
                print(f"[JsonPromptNode] Loaded preset: {json_filename}")
            except Exception as e:
                print(f"[JsonPromptNode] Error loading JSON: {e}")
        else:
            # 文件不存在（或者是占位符），跳过
            pass

        # --- 3. 处理自定义文本 ---
        if custom_text and custom_text.strip() != "":
            parts.append(custom_text)

        # --- 4. 合并输出 ---
        final_output = ", ".join([p.strip() for p in parts if p.strip()])
        
        return (final_output,)

# 映射保留
NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "Advanced JSON Prompt Loader"
}
