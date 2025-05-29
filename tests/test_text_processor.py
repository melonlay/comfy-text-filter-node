import unittest
import sys
import os

# 添加父目錄到路徑以便導入模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.text_processor import TextProcessor


class TestTextProcessor(unittest.TestCase):
    """
    TextProcessor類的單元測試
    """
    
    def setUp(self):
        """測試前的設置"""
        self.processor = TextProcessor()
    
    def test_basic_filtering(self):
        """測試基本過濾功能 - 完全匹配項目"""
        input_prompt = "beautiful girl, red, blue eyes, anime style"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "beautiful girl, blue eyes, anime style"
        
        self.assertEqual(result, expected)
    
    def test_case_insensitive_filtering(self):
        """測試不區分大小寫的過濾"""
        input_prompt = "Beautiful Girl, RED, Blue Eyes, Anime Style"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "Beautiful Girl, Blue Eyes, Anime Style"
        
        self.assertEqual(result, expected)
    
    def test_partial_word_filtering(self):
        """測試部分詞彙不會被過濾（只有完全匹配的項目才過濾）"""
        input_prompt = "redhead, blue sky, greenery"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "redhead, blue sky, greenery"
        
        self.assertEqual(result, expected)
    
    def test_no_substring_match(self):
        """測試不匹配子字串的情況"""
        input_prompt = "bluish, orange, greenery"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "bluish, orange, greenery"
        
        self.assertEqual(result, expected)
    
    def test_empty_input(self):
        """測試空輸入"""
        result = self.processor.filter_prompt("", "red, blue")
        self.assertEqual(result, "")
        
        result = self.processor.filter_prompt("test", "")
        self.assertEqual(result, "test")
    
    def test_no_matches(self):
        """測試沒有匹配的情況"""
        input_prompt = "beautiful girl, anime style"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "beautiful girl, anime style"
        
        self.assertEqual(result, expected)
    
    def test_all_filtered(self):
        """測試全部被過濾的情況"""
        input_prompt = "red, blue"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = ""
        
        self.assertEqual(result, expected)
    
    def test_preserve_word_spacing(self):
        """測試保留單字間空格 - 只有完全匹配的項目才被過濾"""
        input_prompt = "beautiful red girl, blue eyed cat, green tree, red, blue"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "beautiful red girl, blue eyed cat, green tree"
        
        self.assertEqual(result, expected)
    
    def test_simple_brackets(self):
        """測試簡單括號處理"""
        input_prompt = "(hi, I, am, a, girl)"
        filter_words = "girl, hi"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "(I, am, a)"
        
        self.assertEqual(result, expected)
    
    def test_nested_brackets_empty_inner(self):
        """測試嵌套括號，內層變空的情況"""
        input_prompt = "(hi, I, am, a, (girl))"
        filter_words = "girl, hi"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "(I, am, a)"
        
        self.assertEqual(result, expected)
    
    def test_nested_brackets_with_content(self):
        """測試嵌套括號，內層還有內容的情況"""
        input_prompt = "(hi, I, am, (a, girl))"
        filter_words = "girl, hi"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "(I, am, (a))"
        
        self.assertEqual(result, expected)
    
    def test_weight_syntax(self):
        """測試權重語法"""
        input_prompt = "((1girl, loli, a cute loli dancing on the street, nude, NSFW):1.2)"
        filter_words = "nude, NSFW"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "((1girl, loli, a cute loli dancing on the street):1.2)"
        
        self.assertEqual(result, expected)
    
    def test_multiple_bracket_types(self):
        """測試多種括號類型"""
        input_prompt = "[hi, I], {am, girl}, (a, test)"
        filter_words = "girl, hi"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "[I], {am}, (a, test)"
        
        self.assertEqual(result, expected)
    
    def test_completely_empty_brackets(self):
        """測試完全空的括號"""
        input_prompt = "(girl, hi), (test, ok)"
        filter_words = "girl, hi"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "(test, ok)"
        
        self.assertEqual(result, expected)
    
    def test_weight_keyword_filtering(self):
        """測試帶權重的關鍵詞過濾"""
        input_prompt = "((1girl, JK, a cute JK wearing serafuku dancing on the street, nude, (NSFW:1.1), black and white serafuku):1.2)"
        filter_words = "nude, NSFW, loli"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "((1girl, JK, a cute JK wearing serafuku dancing on the street, black and white serafuku):1.2)"
        
        self.assertEqual(result, expected)
    
    def test_various_weight_formats(self):
        """測試各種權重格式"""
        input_prompt = "(red:1.5), (blue:0.8), green, (yellow:2.0)"
        filter_words = "red, blue"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "green, (yellow:2.0)"
        
        self.assertEqual(result, expected)
    
    def test_weight_keyword_case_insensitive(self):
        """測試權重關鍵詞的大小寫不敏感"""
        input_prompt = "(RED:1.5), (Blue:0.8), (NSFW:1.2)"
        filter_words = "red, blue, nsfw"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = ""
        
        self.assertEqual(result, expected)
    
    def test_mixed_weight_and_normal(self):
        """測試混合權重和普通關鍵詞"""
        input_prompt = "beautiful girl, (red:1.5), blue eyes, (nude:0.8), anime style"
        filter_words = "red, nude"
        
        result = self.processor.filter_prompt(input_prompt, filter_words)
        expected = "beautiful girl, blue eyes, anime style"
        
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main() 