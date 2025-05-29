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
        if not input_prompt:
            return input_prompt
            
        # 解析要過濾的詞彙
        filter_set = self._parse_filter_words(filter_words) if filter_words else set()
        
        result = input_prompt
        
        # 步驟1: 移除匹配的關鍵字（包括帶權重的）
        if filter_set:
            result = self._remove_matching_keywords(result, filter_set)
        
        # 步驟2: 後處理清理（總是執行，清理孤立權重等）
        result = self._post_process_cleanup(result)
        
        # 步驟3: 格式化空格
        result = self._format_spacing(result)
        
        return result.strip()
    
    def _parse_filter_words(self, filter_words: str) -> Set[str]:
        """解析要過濾的詞彙為集合"""
        words = [word.strip().lower() for word in filter_words.split(self.separator)]
        return {word for word in words if word}
    
    def _remove_matching_keywords(self, text: str, filter_set: Set[str]) -> str:
        """移除匹配的關鍵字，包括帶權重的格式"""
        # 處理括號結構
        result = self._process_brackets_and_filter(text, filter_set)
        return result
    
    def _process_brackets_and_filter(self, text: str, filter_set: Set[str]) -> str:
        """處理括號結構並過濾關鍵字"""
        result = []
        i = 0
        
        while i < len(text):
            if text[i] in '([{':
                # 找到匹配的結束括號
                bracket_start = i
                bracket_end = self._find_matching_bracket(text, i)
                
                if bracket_end != -1:
                    # 提取括號內容
                    bracket_type = text[i]
                    inner_content = text[i+1:bracket_end]
                    
                    # 檢查括號後是否有權重
                    weight = ""
                    next_pos = bracket_end + 1
                    if next_pos < len(text) and text[next_pos] == ':':
                        weight_match = re.match(r':[\d.]+', text[next_pos:])
                        if weight_match:
                            weight = weight_match.group()
                            next_pos += len(weight)
                    
                    # 遞歸處理括號內容
                    filtered_inner = self._process_brackets_and_filter(inner_content, filter_set)
                    
                    # 如果過濾後還有內容，保留括號
                    if filtered_inner.strip():
                        closing_bracket = self._get_closing_bracket(bracket_type)
                        result.append(bracket_type + filtered_inner + closing_bracket + weight)
                    
                    i = next_pos
                else:
                    # 找不到匹配括號，直接添加
                    result.append(text[i])
                    i += 1
            else:
                # 處理普通文字段落
                segment_end = self._find_next_bracket(text, i)
                segment = text[i:segment_end]
                
                if segment:
                    # 過濾這個段落
                    filtered_segment = self._filter_comma_separated_items(segment, filter_set)
                    result.append(filtered_segment)
                
                i = segment_end
        
        return ''.join(result)
    
    def _filter_comma_separated_items(self, text: str, filter_set: Set[str]) -> str:
        """過濾逗號分隔的項目"""
        if not text.strip():
            return text
            
        # 分割項目
        items = text.split(',')
        filtered_items = []
        
        for item in items:
            item_stripped = item.strip()
            if item_stripped:
                # 檢查是否應該過濾
                should_filter = self._should_filter_item(item_stripped, filter_set)
                if not should_filter:
                    filtered_items.append(item)
            else:
                # 保留空項目（用於保持格式）
                filtered_items.append(item)
        
        return ','.join(filtered_items)
    
    def _should_filter_item(self, item: str, filter_set: Set[str]) -> bool:
        """判斷項目是否應該被過濾"""
        item_lower = item.lower()
        
        # 檢查完全匹配
        if item_lower in filter_set:
            return True
        
        # 檢查權重語法：keyword:number
        weight_match = re.match(r'^(.+?):([\d.]+)$', item_lower)
        if weight_match:
            keyword = weight_match.group(1)
            if keyword in filter_set:
                return True
        
        return False
    
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
    
    def _post_process_cleanup(self, text: str) -> str:
        """後處理清理：移除空括號、重複逗號、孤立權重"""
        # 重複清理直到沒有變化
        prev_text = ""
        while prev_text != text:
            prev_text = text
            
            # 移除空括號
            text = re.sub(r'\(\s*\)', '', text)
            text = re.sub(r'\[\s*\]', '', text)
            text = re.sub(r'\{\s*\}', '', text)
            
            # 移除孤立的權重（只移除括號內只有權重的情況）
            text = re.sub(r'\(\s*:[\d.]+\s*\)', '', text)
            
            # 移除重複的逗號
            text = re.sub(r',\s*,+', ',', text)
            
            # 移除開頭和結尾的逗號
            text = re.sub(r'^\s*,+|,+\s*$', '', text)
            
            # 移除括號內開頭和結尾的逗號
            text = re.sub(r'([(\[{])\s*,', r'\1', text)
            text = re.sub(r',\s*([)\]}])', r'\1', text)
            
            # 修正括號內開頭的多餘空格
            text = re.sub(r'([(\[{])\s+', r'\1', text)
        
        return text
    
    def _format_spacing(self, text: str) -> str:
        """格式化空格：在逗號後添加空格"""
        # 標準化空格
        text = re.sub(r'\s+', ' ', text)
        
        # 確保逗號後有空格（但不在括號內的結尾）
        text = re.sub(r',(?!\s)', ', ', text)
        
        # 修正多餘的空格
        text = re.sub(r'\s+', ' ', text)
        
        return text 