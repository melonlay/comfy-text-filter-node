from ..utils.text_processor import TextProcessor
from ..config.node_config import NodeConfig


class PromptFilterNode:
    """
    ComfyUI節點：用於過濾prompt中的特定詞彙
    
    功能：
    - 接收輸入的prompt字串
    - 根據過濾詞彙列表移除相應的詞彙
    - 輸出過濾後的prompt
    """
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.config = NodeConfig()
    
    @classmethod
    def INPUT_TYPES(cls):
        """定義節點的輸入類型"""
        return {
            "required": {
                "input_prompt": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "輸入要處理的prompt..."
                }),
                "filter_words": ("STRING", {
                    "multiline": True,
                    "default": "",
                    "placeholder": "輸入要過濾的詞彙，用逗號分隔..."
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("filtered_prompt",)
    FUNCTION = "filter_prompt"
    CATEGORY = "text/prompt"
    
    def filter_prompt(self, input_prompt, filter_words):
        """
        過濾prompt的主要功能
        
        Args:
            input_prompt (str): 輸入的prompt
            filter_words (str): 要過濾的詞彙列表
            
        Returns:
            tuple: 包含過濾後prompt的元組
        """
        try:
            # 使用文字處理器進行過濾
            filtered_result = self.text_processor.filter_prompt(
                input_prompt, 
                filter_words
            )
            
            return (filtered_result,)
            
        except Exception as e:
            print(f"Error in PromptFilterNode: {str(e)}")
            return (input_prompt,)  # 發生錯誤時返回原始prompt 