import re
from typing import Set


class TextProcessor:
    """
    文字處理工具類
    
    負責處理prompt的過濾、清理和格式化，支援括號結構處理
    """
    
    def __init__(self):
        self.separator = ","
        
    def filter_prompt(self, input_prompt: str, filter_words: str) -> str:
        """
        過濾prompt中的特定詞彙，保持括號結構
        
        Args:
            input_prompt (str): 輸入的prompt
            filter_words (str): 要過濾的詞彙，用逗號分隔
            
        Returns:
            str: 過濾後的prompt
        """
        if not input_prompt or not filter_words:
            return input_prompt
            
        # 解析要過濾的詞彙
        filter_set = self._parse_filter_words(filter_words)
        
        result = input_prompt
        
        # 步驟1: 移除所有逗號以及括號前後的空格
        result = self._normalize_spaces(result)
        
        # 步驟2: 按逗號分割項目進行完全匹配過濾
        result = self._filter_by_comma_separated_items(result, filter_set)
        
        # 步驟3: 移除所有空括號和連續逗號
        result = self._clean_empty_brackets_and_commas(result)
        
        # 步驟4: 恢復逗號後的空格格式
        result = self._restore_comma_spacing(result)
        
        return result.strip()
    
    def _parse_filter_words(self, filter_words: str) -> Set[str]:
        """解析要過濾的詞彙為集合"""
        words = [word.strip().lower() for word in filter_words.split(self.separator)]
        return {word for word in words if word}
    
    def _normalize_spaces(self, text: str) -> str:
        """步驟1: 移除所有逗號以及括號前後的空格"""
        # 移除括號前後的空格
        text = re.sub(r'\s*([(\[{])\s*', r'\1', text)
        text = re.sub(r'\s*([)\]}])\s*', r'\1', text)
        # 移除逗號前後的空格
        text = re.sub(r'\s*,\s*', ',', text)
        return text
    
    def _filter_by_comma_separated_items(self, text: str, filter_set: Set[str]) -> str:
        """步驟2: 按逗號分割的項目進行完全匹配過濾"""
        # 遞歸處理括號內容
        return self._process_text_recursive(text, filter_set)
    
    def _process_text_recursive(self, text: str, filter_set: Set[str]) -> str:
        """遞歸處理文字，處理括號結構"""
        result = []
        i = 0
        
        while i < len(text):
            if text[i] in '([{':
                # 處理括號
                bracket_type = text[i]
                bracket_end = self._find_matching_bracket(text, i)
                
                if bracket_end != -1:
                    # 提取括號內容
                    inner_content = text[i+1:bracket_end]
                    
                    # 檢查權重語法
                    weight = ""
                    next_pos = bracket_end + 1
                    if next_pos < len(text) and text[next_pos] == ':':
                        weight_match = re.match(r':[\d.]+', text[next_pos:])
                        if weight_match:
                            weight = weight_match.group()
                            next_pos += len(weight)
                    
                    # 遞歸處理括號內容
                    processed_inner = self._process_text_recursive(inner_content, filter_set)
                    
                    # 如果處理後還有內容，保留括號
                    if processed_inner.strip():
                        closing_bracket = self._get_closing_bracket(bracket_type)
                        result.append(bracket_type + processed_inner + closing_bracket + weight)
                    
                    i = next_pos
                else:
                    # 找不到匹配括號，直接添加
                    result.append(text[i])
                    i += 1
            else:
                # 處理普通文字，直到下一個括號
                segment_end = self._find_next_bracket(text, i)
                segment = text[i:segment_end]
                
                if segment.strip():
                    filtered_segment = self._filter_comma_separated_segment(segment, filter_set)
                    if filtered_segment:
                        result.append(filtered_segment)
                
                i = segment_end
        
        return ''.join(result)
    
    def _filter_comma_separated_segment(self, segment: str, filter_set: Set[str]) -> str:
        """過濾逗號分割的段落"""
        # 按逗號分割
        items = segment.split(',')
        filtered_items = []
        
        for item in items:
            if item:  # 跳過空項目
                # 檢查是否完全匹配過濾詞彙（不區分大小寫）
                item_lower = item.lower()
                should_filter = item_lower in filter_set
                
                if not should_filter:
                    filtered_items.append(item)
        
        return ','.join(filtered_items)
    
    def _find_matching_bracket(self, text: str, start: int) -> int:
        """找到匹配的結束括號"""
        open_bracket = text[start]
        close_bracket = self._get_closing_bracket(open_bracket)
        
        count = 1
        i = start + 1
        
        while i < len(text) and count > 0:
            if text[i] == open_bracket:
                count += 1
            elif text[i] == close_bracket:
                count -= 1
            i += 1
        
        return i - 1 if count == 0 else -1
    
    def _get_closing_bracket(self, open_bracket: str) -> str:
        """獲取對應的結束括號"""
        bracket_map = {'(': ')', '[': ']', '{': '}'}
        return bracket_map.get(open_bracket, ')')
    
    def _find_next_bracket(self, text: str, start: int) -> int:
        """找到下一個括號的位置"""
        i = start
        while i < len(text) and text[i] not in '([{':
            i += 1
        return i
    
    def _clean_empty_brackets_and_commas(self, text: str) -> str:
        """步驟3: 移除所有空括號和連續逗號"""
        # 重複清理直到沒有變化
        prev_text = ""
        while prev_text != text:
            prev_text = text
            
            # 移除空括號 (包括只有空格的括號)
            text = re.sub(r'\(\s*\)', '', text)
            text = re.sub(r'\[\s*\]', '', text)
            text = re.sub(r'\{\s*\}', '', text)
            
            # 移除連續逗號
            text = re.sub(r',+', ',', text)
            
            # 移除開頭和結尾的逗號
            text = re.sub(r'^,+|,+$', '', text)
            
            # 移除括號前後多餘的逗號
            text = re.sub(r',+([(\[{])', r'\1', text)
            text = re.sub(r'([)\]}]),+', r'\1', text)
            
            # 移除括號內尾隨的逗號
            text = re.sub(r',+([)\]}])', r'\1', text)
            
            # 移除括號前的逗號（當括號前沒有其他內容時）
            text = re.sub(r'^([(\[{])', r'\1', text)
        
        return text
    
    def _restore_comma_spacing(self, text: str) -> str:
        """步驟4: 恢復逗號後的空格格式"""
        # 在逗號後添加空格，但不在括號前
        text = re.sub(r',(?![)\]}])', ', ', text)
        
        # 處理括號間的分隔：如果兩個元素之間沒有逗號，添加逗號和空格
        # 匹配：字母/數字 + 括號 或 括號 + 字母/數字
        text = re.sub(r'([a-zA-Z0-9])([(\[{])', r'\1, \2', text)
        text = re.sub(r'([)\]}])([a-zA-Z0-9])', r'\1, \2', text)
        text = re.sub(r'([)\]}])([(\[{])', r'\1, \2', text)
        
        return text 