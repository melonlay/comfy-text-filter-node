# ComfyUI Prompt Filter Node 安裝指南

## 系統需求

- Python 3.7+
- ComfyUI (最新版本)

## 安裝步驟

### 方法1: 直接複製 (推薦)

1. **下載專案**
   ```bash
   git clone https://github.com/melonlay/comfy-text-filter-node.git prompt_filter
   ```

2. **複製到ComfyUI**
   將整個 `prompt_filter` 資料夾複製到您的ComfyUI安裝目錄下的 `custom_nodes` 資料夾中：
   ```
   ComfyUI/
   └── custom_nodes/
       └── prompt_filter/
           ├── __init__.py
           ├── nodes/
           ├── utils/
           ├── config/
           └── ...
   ```

3. **重新啟動ComfyUI**
   重新啟動ComfyUI應用程式

4. **驗證安裝**
   在ComfyUI的節點列表中尋找 "Prompt Filter" 節點

### 方法2: 符號連結 (開發者)

如果您想要開發或修改這個節點：

1. **克隆專案到開發目錄**
   ```bash
   git clone https://github.com/melonlay/comfy-text-filter-node.git /path/to/your/dev/prompt_filter
   ```

2. **創建符號連結**
   ```bash
   # Windows (以管理員身份運行)
   mklink /D "C:\path\to\ComfyUI\custom_nodes\prompt_filter" "C:\path\to\your\dev\prompt_filter"
   
   # Linux/Mac
   ln -s /path/to/your/dev/prompt_filter /path/to/ComfyUI/custom_nodes/prompt_filter
   ```

## 過濾邏輯說明

此節點使用**按逗號分割項目的完全匹配**邏輯：

- **完全匹配**: 只有與過濾詞彙完全匹配的項目才會被移除
- **逗號分割**: 以逗號為分隔符來識別不同的項目
- **保留結構**: 保持括號結構和權重語法

### 範例說明

- 輸入: `"beautiful girl, red, blue eyes, anime style"`
- 過濾: `"red, blue"`
- 輸出: `"beautiful girl, blue eyes, anime style"`
- 說明: 只有完全匹配的 `"red"` 被移除，`"blue eyes"` 保留

## 驗證安裝

### 1. 檢查節點是否載入

啟動ComfyUI後，檢查控制台輸出是否有錯誤訊息。

### 2. 尋找節點

在ComfyUI界面中：
1. 右鍵點擊空白區域
2. 選擇 "Add Node"
3. 導航到 "text" → "prompt" → "Prompt Filter"

### 3. 測試功能

1. 添加 "Prompt Filter" 節點
2. 在 "input_prompt" 欄位輸入: `beautiful girl, red, blue eyes, anime style`
3. 在 "filter_words" 欄位輸入: `red, blue`
4. 執行工作流程
5. 確認輸出為: `beautiful girl, blue eyes, anime style`

### 4. 測試括號處理

1. 在 "input_prompt" 欄位輸入: `(hi, I, am, a, girl)`
2. 在 "filter_words" 欄位輸入: `girl, hi`
3. 確認輸出為: `(I, am, a)`

### 5. 測試權重語法

1. 在 "input_prompt" 欄位輸入: `((1girl, loli, nude, NSFW):1.2)`
2. 在 "filter_words" 欄位輸入: `nude, NSFW`
3. 確認輸出為: `((1girl, loli):1.2)`

## 故障排除

### 常見問題

**問題1: 節點沒有出現在列表中**
- 確認資料夾結構正確
- 檢查 `__init__.py` 文件是否存在
- 重新啟動ComfyUI
- 檢查控制台是否有錯誤訊息

**問題2: 導入錯誤**
- 確認所有必要的文件都已複製
- 檢查Python路徑設置
- 確認ComfyUI版本相容性

**問題3: 節點執行錯誤**
- 檢查輸入格式是否正確
- 確認過濾詞彙使用逗號分隔
- 查看ComfyUI控制台的錯誤訊息

**問題4: 過濾結果不符合預期**
- 確認理解完全匹配邏輯：只有完全匹配的項目才會被過濾
- 檢查過濾詞彙是否正確拼寫
- 注意大小寫不敏感匹配

### 測試安裝

運行包含的測試來驗證功能：

```bash
cd /path/to/ComfyUI/custom_nodes/prompt_filter
python tests/test_text_processor.py
```

如果所有測試通過，表示安裝成功。

## 更新

要更新到最新版本：

1. 備份您的自定義配置（如果有）
2. 下載最新版本
3. 替換舊文件
4. 重新啟動ComfyUI

## 卸載

要移除這個節點：

1. 刪除 `ComfyUI/custom_nodes/prompt_filter` 資料夾
2. 重新啟動ComfyUI

## 支援

如果遇到問題，請：

1. 檢查這個安裝指南
2. 查看README文件
3. 運行測試來診斷問題
4. 在GitHub上提交Issue並附上錯誤訊息 