from .nodes.prompt_filter_node import PromptFilterNode

# 節點映射
NODE_CLASS_MAPPINGS = {
    "PromptFilterNode": PromptFilterNode
}

# 節點顯示名稱映射
NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptFilterNode": "Prompt Filter"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 