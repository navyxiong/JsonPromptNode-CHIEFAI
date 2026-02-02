import os

# 导入节点类和映射
from .json_prompt_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 自动创建 preset 目录结构
NODE_DIR = os.path.dirname(os.path.abspath(__file__))
PRESET_DIR = os.path.join(NODE_DIR, "preset")

# 确保三个预设子文件夹存在
for sub_folder in ["perspective", "birdview", "others"]:
   target_path = os.path.join(PRESET_DIR, sub_folder)
   os.makedirs(target_path, exist_ok=True)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
