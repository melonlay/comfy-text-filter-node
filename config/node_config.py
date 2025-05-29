class NodeConfig:
    """
    節點配置類
    
    管理節點的各種配置參數
    """
    
    def __init__(self):
        # 節點基本配置
        self.node_name = "Prompt Filter"
        self.node_category = "text/prompt"
        self.version = "1.0.0"
        
        # 文字處理配置
        self.default_separator = ","
        self.case_sensitive = False
        
        # UI配置
        self.input_placeholder = {
            "zh": "輸入要處理的prompt...",
            "en": "Enter prompt to process..."
        }
        
        self.filter_placeholder = {
            "zh": "輸入要過濾的詞彙，用逗號分隔...",
            "en": "Enter words to filter, separated by commas..."
        }
    
    def get_placeholder(self, field: str, language: str = "zh") -> str:
        """
        獲取佔位符文字
        
        Args:
            field (str): 欄位名稱
            language (str): 語言代碼
            
        Returns:
            str: 佔位符文字
        """
        placeholders = {
            "input": self.input_placeholder,
            "filter": self.filter_placeholder
        }
        
        return placeholders.get(field, {}).get(language, "") 