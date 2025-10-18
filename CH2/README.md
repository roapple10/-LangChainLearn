# CH2: LangChain 基礎應用

本章節展示 LangChain 的基礎應用，包括使用不同的 LLM 模型進行各種任務。

## 🔑 API 申請教學

在開始學習前，您需要先取得 AI 模型的 API Key。以下提供兩種選擇：

### 方案一：Azure OpenAI Service（有限制條件）

Azure OpenAI 提供 $200 美金的免費額度，但有**嚴格的限制條件**：

⚠️ **重要限制：必須是全新帳號才能使用免費額度**
- **全新的電話號碼**（之前未註冊過 Azure 服務）
- **全新的信用卡**（之前未綁定過 Azure 帳號）
- **全新的電子信箱**（之前未使用過 Azure 服務）

如果您曾經使用過 Azure 任何服務，即使是免費試用，都**無法再次申請免費額度**。

#### Azure OpenAI 申請步驟

1. 前往 [Azure Portal](https://portal.azure.com/)
2. 使用全新的 Microsoft 帳號註冊
3. 提供信用卡資訊（僅用於驗證，不會自動扣款）
4. 建立 Azure OpenAI 資源
5. 取得 Endpoint 和 API Key

詳細教學請參考：[Azure OpenAI Service 申請教學](https://ithelp.ithome.com.tw/m/articles/10353046)

**如果您不符合全新帳號條件，請改用下方推薦的 Google AI Studio**

---

### 方案二：Google AI Studio API（推薦！免費且簡單）⭐

**為什麼推薦使用 Google AI Studio？**

✅ **完全免費**：無需綁定信用卡  
✅ **設定簡單**：5 分鐘內完成申請  
✅ **無帳號限制**：任何 Google 帳號都能使用  
✅ **慷慨的免費額度**：每分鐘 15 個請求，足夠學習使用  
✅ **強大的 Gemini 模型**：效能媲美 GPT-4

#### Google AI Studio 申請步驟（5 步驟完成）

**第一步**：前往 [Google AI Studio](https://ai.google.dev)，點擊藍色按鈕「Explore models in Google AI Studio」

**第二步**：勾選第一個選項，並點擊「I accept」同意條款

**第三步**：點擊右上角的「Get API key」按鈕

**第四步**：點擊「Create API key」按鈕（或選擇現有的 Google Cloud 專案）

**第五步**：等待幾秒後，您會看到專屬的 API Key，點擊「Copy」複製

🎉 **完成！** 您現在擁有免費的 Gemini API 了

#### Google Gemini 免費額度

| 項目 | 免費額度 |
|------|---------|
| 每分鐘請求數 (RPM) | 15 次 |
| 每日請求數 (RPD) | 1,500 次 |
| 每分鐘 Token 數 (TPM) | 1,000,000 個 |

💡 **這些額度對於學習和開發來說綽綽有餘！**

#### 確認使用的是免費額度

在 Google AI Studio 的 API Key 介面中，確認該 API Key 的 Plan 顯示為 **「Free tier」** 或 **「Unavailable」**，就代表使用的是免費額度，不會被扣款。

詳細圖文教學請參考：[手把手教你申請免費 Google Gemini API](https://lifecheatslab.com/freegeminiapi/)

---

### API 方案比較

| 比較項目 | Azure OpenAI | Google AI Studio |
|---------|-------------|------------------|
| 費用 | 需綁信用卡（$200 免費額度） | 完全免費 |
| 申請難度 | 較複雜 | 非常簡單 |
| 帳號限制 | 必須全新帳號 | 較無限制 |
| 設定時間 | 1-3 分鐘 | 1-3 分鐘 |
| 模型 | GPT-3.5, GPT-4 | Gemini 2.0 |
| 適合對象 | 企業開發 | 學習、個人開發 |


---

## 環境需求

- Python 3.11+
- Poetry（套件管理工具）

## 安裝 Poetry

### macOS / Linux

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Windows (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

安裝完成後，請重新啟動終端機。

## 初始化專案環境

### macOS / Linux

```bash
# 進入 CH2 目錄
cd /Users/ray-mac/Documents/Lanchain/LangChainLearnBook/CH2

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

### Windows

```powershell
# 進入 CH2 目錄
cd C:\Users\YourUsername\Documents\Lanchain\LangChainLearnBook\CH2

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

## 為什麼使用 langchain-google-genai < 3.0.0？

由於當前專案使用的 `langchain-community 0.3.x` 與 `langchain-google-genai 3.0.0` 存在依賴衝突：

- `langchain-google-genai 3.0.0` 需要 `langchain-core >= 1.0.0`
- `langchain-community 0.3.x` 需要 `langchain-core < 1.0.0`

因此我們使用 **2.x 版本**的 `langchain-google-genai`，這個版本與現有依賴完全相容，並且支援所有 Gemini 模型功能。

## 設定環境變數

在專案根目錄建立 `.env` 檔案（Mac 和 Windows 相同）：

```env
# OpenAI API Key（用於 2-2/app.py）
OPENAI_API_KEY=your-openai-api-key-here

# Google Gemini API Key（用於 2-2/app_gemini.py）
GOOGLE_API_KEY=your-google-api-key-here
```

### 取得 API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://makersuite.google.com/app/apikey

## 執行範例程式

### macOS / Linux

```bash
# 執行 OpenAI 範例
poetry run python 2-2/app.py

# 執行 Gemini 範例
poetry run python 2-2/app_gemini.py

# 執行其他章節
poetry run python 2-3/app.py
poetry run python 2-4/app.py
```

### Windows

```powershell
# 執行 OpenAI 範例
poetry run python 2-2/app.py

# 執行 Gemini 範例
poetry run python 2-2/app_gemini.py

# 執行其他章節
poetry run python 2-3/app.py
poetry run python 2-4/app.py
```

## 啟用虛擬環境（進階）

如果您想要直接在虛擬環境中工作：

### macOS / Linux

```bash
### 啟動虛擬環境（Poetry 2.0+）

**重要提示：** 從 Poetry 2.0.0 開始，`poetry shell` 命令不再預設可用。請使用以下新方法：

#### 方法 1：使用 `env activate` 命令（官方推薦）

**步驟 1：** 執行以下命令查看啟動環境的指令：

**Windows (PowerShell) / Mac (Terminal):**
```bash
poetry env activate
```


# 現在可以直接執行 Python 腳本
python 2-2/app.py
python 2-2/app_gemini.py

# 離開虛擬環境
exit
```

### Windows

```powershell
# 啟用虛擬環境
poetry shell

# 現在可以直接執行 Python 腳本
poetry run python 2-2/app.py
poetry run python 2-2/app_gemini.py

# 離開虛擬環境
exit
```

## 章節說明

### 2-2: LLM 基礎使用
- `app.py`: 使用 OpenAI GPT 模型進行翻譯
- `app_gemini.py`: 使用 Google Gemini 模型進行翻譯

### 2-3: Prompt Templates
- 使用 LangChain 的 Prompt Templates 功能

### 2-4: Output Parsers
- 解析和結構化 LLM 輸出

## 故障排除

### 問題：找不到 poetry 命令

**解決方法**：
- macOS/Linux: 將 `export PATH="$HOME/.local/bin:$PATH"` 加入 `~/.bashrc` 或 `~/.zshrc`
- Windows: 確認 Poetry 的安裝路徑已加入系統 PATH

### 問題：ModuleNotFoundError

**解決方法**：
```bash
# 確認在正確的目錄
cd /path/to/LangChainLearnBook/CH2

# 重新安裝依賴
poetry install
```

### 問題：API Key 錯誤

**解決方法**：
1. 確認 `.env` 檔案位於 CH2 目錄
2. 確認 API Key 沒有多餘的空格或引號
3. 確認 API Key 仍然有效且有配額

### 問題：依賴版本衝突

**解決方法**：
```bash
# 清除鎖定檔案
rm poetry.lock

# 重新解析依賴
poetry install

# 重新安裝 Google Gemini 支援
poetry add "langchain-google-genai<3.0.0"
```

## 相關資源

- [LangChain 官方文檔](https://python.langchain.com/)
- [Poetry 官方文檔](https://python-poetry.org/docs/)
- [Google Gemini API 文檔](https://ai.google.dev/docs)
- [OpenAI API 文檔](https://platform.openai.com/docs)

## 注意事項

- 本專案使用 Poetry 進行依賴管理，建議不要混用 pip
- API Keys 請勿上傳至版本控制系統（`.env` 已在 `.gitignore` 中）
- 使用 API 前請確認服務商的定價和配額限制

