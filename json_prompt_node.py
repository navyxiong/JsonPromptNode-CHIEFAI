import os
import json
import folder_paths
import time
import random

# 定义三个预设对应的子文件夹（键名改为中文）
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
        # 获取当前节点文件所在目录，并在其下创建 preset 文件夹路径
        node_dir = os.path.dirname(os.path.abspath(__file__))
        self.preset_root = os.path.join(node_dir, "preset")

    @classmethod
    def INPUT_TYPES(s):
        # 获取当前节点文件所在目录下的 preset 路径
        node_dir = os.path.dirname(os.path.abspath(__file__))
        preset_root = os.path.join(node_dir, "preset")
        optional_inputs = {}

        # 为每个预设创建对应的文件列表
        for preset_name, sub_folder in PRESET_FOLDERS.items():
            target_dir = os.path.join(preset_root, sub_folder)
            
            # 确保目录存在
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir, exist_ok=True)
                except Exception as e:
                    print(f"[JsonPromptNode] Warning: Could not create directory {target_dir}: {e}")

            # 读取该文件夹下的 json 文件
            files = ["None"]
            if os.path.exists(target_dir):
                try:
                    json_files = [f for f in os.listdir(target_dir) if f.endswith(".json")]
                    files.extend(sorted(json_files))
                except Exception as e:
                    print(f"[JsonPromptNode] Error reading directory {target_dir}: {e}")

            # 添加标记 "searchable" 供前端识别，启用搜索功能
            optional_inputs[preset_name] = (files, {
                "searchable": True,
                "tooltip": f"从 {sub_folder}/ 文件夹选择 JSON 文件"
            })

        return {
            "required": {
                "custom_text": ("STRING", {
                    "multiline": True, 
                    "default": "", 
                    "placeholder": "在此输入自定义提示词..."
                }),
                "enable_default_prompt": ("BOOLEAN", {
                    "default": True, 
                    "label_on": "启用默认提示词", 
                    "label_off": "禁用默认提示词"
                }),
                # 新增：缓存释放按钮
                "释放缓存": ("BOOLEAN", {
                    "default": False,
                    "label_on": "强制刷新", 
                    "label_off": "正常执行"
                }),
            },
            "optional": optional_inputs
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("final_prompt",)
    FUNCTION = "process_prompts"
    CATEGORY = "utils/prompt_loaders"
    OUTPUT_NODE = False
    
    DESCRIPTION = "从指定文件夹加载 JSON 预设，支持可搜索下拉菜单和缓存释放"

    @classmethod
    def IS_CHANGED(cls, custom_text, enable_default_prompt, 释放缓存, **kwargs):
        """
        控制 ComfyUI 缓存机制的关键方法。
        当返回的值与上一次不同时，ComfyUI 会强制重新执行节点。
        """
        # 如果用户勾选了"释放缓存"，返回随机值强制刷新
        if 释放缓存:
            return float("nan")  # NaN 永远不等于任何值（包括自身），强制刷新
        
        # 正常状态下，基于文件修改时间戳返回一个标识符
        # 这样可以自动检测 JSON 文件是否被外部修改
        node_dir = os.path.dirname(os.path.abspath(__file__))
        preset_root = os.path.join(node_dir, "preset")
        mtime_hash = []
        
        for sub_folder in PRESET_FOLDERS.values():
            target_dir = os.path.join(preset_root, sub_folder)
            if os.path.exists(target_dir):
                try:
                    # 读取文件夹修改时间作为简易指纹
                    mtime = os.path.getmtime(target_dir)
                    mtime_hash.append(f"{sub_folder}:{mtime}")
                except:
                    pass
        
        # 结合输入参数生成指纹
        return hash((
            custom_text, 
            enable_default_prompt, 
            tuple(mtime_hash),
            time.time() // 10  # 每 10 秒允许一次自然刷新（可选，如需严格缓存可删除此行）
        ))

    def load_preset(self, filename, sub_folder):
        """从指定子文件夹加载预设"""
        if not filename or filename == "None":
            return None
        
        file_path = os.path.join(self.preset_root, sub_folder, filename)
        
        if not os.path.exists(file_path):
            print(f"[JsonPromptNode] Warning: File not found: {file_path}")
            return None
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, list):
                    return ", ".join([str(item) for item in data])
                elif isinstance(data, dict):
                    return ", ".join([str(v) for v in data.values()])
                else:
                    return str(data)
                    
        except json.JSONDecodeError as e:
            print(f"[JsonPromptNode] Error: Invalid JSON in {filename}: {e}")
            return None
        except Exception as e:
            print(f"[JsonPromptNode] Error loading {filename}: {e}")
            return None

    def process_prompts(self, custom_text, enable_default_prompt, 释放缓存, 透视图="None", 鸟瞰图="None", 其他="None"):
        parts = []
        
        # 如果触发了强制刷新，打印日志提示
        if 释放缓存:
            print("[JsonPromptNode] 强制刷新缓存，重新读取 JSON 文件...")

        # 1. 添加默认提示词
        if enable_default_prompt:
            parts.append(DEFAULT_PROMPT_TEXT)

        # 2. 处理三个预设（分别对应不同文件夹）
        preset_values = {
            "透视图": 透视图,
            "鸟瞰图": 鸟瞰图,
            "其他": 其他
        }
        
        for preset_key, filename in preset_values.items():
            sub_folder = PRESET_FOLDERS[preset_key]
            content = self.load_preset(filename, sub_folder)
            if content:
                parts.append(content)

        # 3. 添加自定义文本
        if custom_text and custom_text.strip():
            parts.append(custom_text.strip())

        # 4. 合并结果
        final_output = ", ".join([p.strip() for p in parts if p and p.strip()])
        
        return (final_output,)

NODE_CLASS_MAPPINGS = {
    "JsonPromptNode": JsonPromptNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "JsonPromptNode": "高级 JSON 提示词加载器 (缓存释放版)"
}
