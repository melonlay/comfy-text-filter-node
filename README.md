# ComfyUI Prompt Filter 節點

一個用於ComfyUI的自定義節點，可以過濾prompt中的特定詞彙，同時保持括號結構和權重語法。

## 功能特點

- **完全匹配過濾**: 只有與過濾詞彙完全匹配的項目（按逗號分割）才會被移除
- **括號結構保持**: 支援圓括號 `()`、方括號 `[]`、花括號 `{}`
- **權重語法支援**: 保持 `:1.2` 等權重語法
- **嵌套括號處理**: 正確處理多層嵌套的括號結構
- **自動清理**: 移除空括號和多餘的逗號

## 過濾邏輯

該節點使用**按逗號分割項目的完全匹配**邏輯：

### 範例說明

1. **基本過濾**:
   - 輸入: `"beautiful girl, red, blue eyes, anime style"`
   - 過濾詞: `"red, blue"`
   - 輸出: `"beautiful girl, blue eyes, anime style"`
   - 說明: 只有完全匹配的 `"red"` 被移除，`"blue eyes"` 保留

2. **部分匹配不被過濾**:
   - 輸入: `"red dress, red hair"`
   - 過濾詞: `"red"`
   - 輸出: `"red dress, red hair"`
   - 說明: `"red dress"` 和 `"red hair"` 不是完全匹配 `"red"`，所以保留

3. **括號處理**:
   - 輸入: `"(hi, I, am, a, girl)"`
   - 過濾詞: `"girl, hi"`
   - 輸出: `"(I, am, a)"`

4. **權重語法**:
   - 輸入: `"((1girl, loli, nude, NSFW):1.2)"`
   - 過濾詞: `"nude, NSFW"`
   - 輸出: `"((1girl, loli):1.2)"`

## 安裝方法

詳見 [INSTALL.md](INSTALL.md)

## 使用方法

1. 在ComfyUI中添加 "Prompt Filter" 節點
2. 連接文字輸入到 `input_prompt` 
3. 在 `filter_words` 參數中輸入要過濾的詞彙（用逗號分隔）
4. 從 `output_prompt` 獲取過濾後的結果

## 項目結構

```
prompt_filter/
├── __init__.py                 # 模組初始化
├── nodes/
│   └── prompt_filter_node.py  # ComfyUI節點實現
├── utils/
│   └── text_processor.py      # 文字處理邏輯
├── config/
│   └── node_config.py         # 節點配置
├── tests/
│   └── test_text_processor.py # 單元測試
├── README.md                   # 中文說明文件
├── README_EN.md               # 英文說明文件
└── INSTALL.md                 # 安裝說明
```

## 技術特點

1. **原子化設計**: 每個模組職責單一，便於維護
2. **樹狀結構**: 清晰的目錄組織
3. **低耦合**: 模組間依賴最小化
4. **雙語支援**: 中英文文檔
5. **使用者友善**: 簡單易用的介面

## 測試

運行測試套件：
```bash
python tests/test_text_processor.py
```

## 授權

GPL-3.0 License 