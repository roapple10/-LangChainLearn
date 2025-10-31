# CH4: LangChain Chains 進階應用

本章節深入探討 LangChain 的 Chain 機制，學習如何將多個任務串接成複雜的工作流程，包括 Sequential Chain（順序鏈）、Router Chain（路由鏈）和 Conditional Chain（條件鏈）等進階應用。

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

### 方案二：Google AI Studio API

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
| 模型 | GPT 模型 | Gemini 模型 |

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
# 進入 CH4/demo1 目錄（從專案根目錄）
cd python_langchain_gemini_azure/CH4/demo1

# 安裝基礎依賴
poetry install

# 安裝 Google Gemini 支援（選項 A：使用相容版本）
poetry add "langchain-google-genai<3.0.0"
```

### Windows

```powershell
# 進入 CH4/demo1 目錄（從專案根目錄）
cd python_langchain_gemini_azure\CH4\demo1

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
# Azure OpenAI 設定（用於 demo1/app.py, demo4-1.py 到 demo4-7.py）
AZURE_OPENAI_ENDPOINT=your-azure-endpoint-here
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name-here
AZURE_OPENAI_DEPLOYMENT_NAME_EMBEDDING=your-embedding-deployment-name-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_KEY=your-azure-api-key-here

# Google Gemini API Key（用於 demo1/app_gemini.py, demo4-1_gemini.py 到 demo4-7_gemini.py）
GOOGLE_API_KEY=your-google-api-key-here
GEMINI_MODEL_ID=gemini-1.5-flash-latest
```

### 取得 API Keys

- **Azure OpenAI**: https://portal.azure.com/（需要建立 Azure OpenAI 資源）
- **Google Gemini**: https://ai.google.dev/（推薦使用，免費且無需信用卡）

## 執行範例程式

### macOS / Linux

```bash
# demo4-1: LLMChain 基礎用法
poetry run python demo1/app.py              # Azure OpenAI 版本
poetry run python demo1/app_gemini.py       # Google Gemini 版本
poetry run python demo1/demo4-1.py          # Azure OpenAI 版本
poetry run python demo1/demo4-1_gemini.py   # Google Gemini 版本

# demo4-2: SimpleSequentialChain（簡單順序鏈）
poetry run python demo1/demo4-2.py          # Azure OpenAI 版本
poetry run python demo1/demo4-2_gemini.py   # Google Gemini 版本

# demo4-3: SequentialChain（三步驟：描述→旅遊建議→翻譯）
poetry run python demo1/demo4-3.py          # Azure OpenAI 版本
poetry run python demo1/demo4-3_gemini.py   # Google Gemini 版本

# demo4-4: SequentialChain（四步驟：描述→氣候→旅遊建議→翻譯）
poetry run python demo1/demo4-4.py          # Azure OpenAI 版本
poetry run python demo1/demo4-4_gemini.py   # Google Gemini 版本

# demo4-5: SequentialChain（動態月份輸入）
poetry run python demo1/demo4-5.py          # Azure OpenAI 版本
poetry run python demo1/demo4-5_gemini.py   # Google Gemini 版本

# demo4-6: MultiPromptChain（路由鏈：翻譯/寫作/一般問答）
poetry run python demo1/demo4-6.py          # Azure OpenAI 版本
poetry run python demo1/demo4-6_gemini.py   # Google Gemini 版本

# demo4-7: Conditional Chain（條件鏈：情緒分析與回應）
poetry run python demo1/demo4-7.py          # Azure OpenAI 版本
poetry run python demo1/demo4-7_gemini.py   # Google Gemini 版本
```

### Windows

```powershell
# demo4-1: LLMChain 基礎用法
poetry run python demo1/app.py              # Azure OpenAI 版本
poetry run python demo1/app_gemini.py       # Google Gemini 版本
poetry run python demo1/demo4-1.py          # Azure OpenAI 版本
poetry run python demo1/demo4-1_gemini.py   # Google Gemini 版本

# demo4-2: SimpleSequentialChain（簡單順序鏈）
poetry run python demo1/demo4-2.py          # Azure OpenAI 版本
poetry run python demo1/demo4-2_gemini.py   # Google Gemini 版本

# demo4-3: SequentialChain（三步驟：描述→旅遊建議→翻譯）
poetry run python demo1/demo4-3.py          # Azure OpenAI 版本
poetry run python demo1/demo4-3_gemini.py   # Google Gemini 版本

# demo4-4: SequentialChain（四步驟：描述→氣候→旅遊建議→翻譯）
poetry run python demo1/demo4-4.py          # Azure OpenAI 版本
poetry run python demo1/demo4-4_gemini.py   # Google Gemini 版本

# demo4-5: SequentialChain（動態月份輸入）
poetry run python demo1/demo4-5.py          # Azure OpenAI 版本
poetry run python demo1/demo4-5_gemini.py   # Google Gemini 版本

# demo4-6: MultiPromptChain（路由鏈：翻譯/寫作/一般問答）
poetry run python demo1/demo4-6.py          # Azure OpenAI 版本
poetry run python demo1/demo4-6_gemini.py   # Google Gemini 版本

# demo4-7: Conditional Chain（條件鏈：情緒分析與回應）
poetry run python demo1/demo4-7.py          # Azure OpenAI 版本
poetry run python demo1/demo4-7_gemini.py   # Google Gemini 版本
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
python demo1/app.py
python demo1/app_gemini.py
python demo1/demo4-1.py
python demo1/demo4-1_gemini.py
python demo1/demo4-2.py
python demo1/demo4-2_gemini.py
# ... 以此類推

# 離開虛擬環境
exit
```

### Windows

```powershell
# 啟用虛擬環境
poetry shell

# 現在可以直接執行 Python 腳本
python demo1/app.py
python demo1/app_gemini.py
python demo1/demo4-1.py
python demo1/demo4-1_gemini.py
python demo1/demo4-2.py
python demo1/demo4-2_gemini.py
# ... 以此類推

# 離開虛擬環境
exit
```

## 章節說明

### demo4-1 / app.py: LLMChain 基礎用法
- `app.py` / `demo4-1.py`: 使用 Azure OpenAI + LLMChain
- `app_gemini.py` / `demo4-1_gemini.py`: 使用 Google Gemini + LLMChain
- **學習重點**：
  - 理解 LLMChain 的基本結構（LLM + Prompt Template）
  - 學習多種 chain 執行方式：`invoke()`, `run()`, `__call__()`
  - 建立簡單的英文翻譯中文功能

### demo4-2: SimpleSequentialChain（簡單順序鏈）
- **學習重點**：
  - 將兩個 LLMChain 串接成順序鏈
  - 第一個 chain 的輸出自動成為第二個 chain 的輸入
  - 實作「描述城市」→「翻譯成英文」的兩步驟流程
  - SimpleSequentialChain 限制：只能傳遞單一輸出

### demo4-3: SequentialChain（三步驟工作流）
- **學習重點**：
  - 使用 SequentialChain 處理多步驟任務
  - 透過 `output_key` 明確定義每個 chain 的輸出變數名稱
  - 實作「描述城市」→「生成旅遊建議」→「翻譯成英文」
  - 學習如何在 chain 之間傳遞具名變數

### demo4-4: SequentialChain（多輸入變數）
- **學習重點**：
  - 同時執行多個 chain 且共用相同的初始輸入
  - 後續 chain 可以使用多個前置 chain 的輸出結果
  - 實作「描述城市」和「描述氣候」並行，再結合兩者生成旅遊建議

### demo4-5: SequentialChain（動態輸入）
- **學習重點**：
  - 在執行時動態提供多個輸入變數
  - 使用 Python `datetime` 模組取得當前月份
  - 實作根據當前月份動態調整氣候描述的智能旅遊建議系統

### demo4-6: MultiPromptChain（路由鏈）
- **學習重點**：
  - 使用 LLM 自動判斷該執行哪個專門的 chain
  - 建立多個專門任務的 chain（翻譯、寫作、一般問答）
  - 透過 RouterChain 實現智能路由選擇
  - 設定 default_chain 處理無法分類的請求

### demo4-7: Conditional Chain（條件鏈）
- **學習重點**：
  - 根據 LLM 分析結果動態決定執行流程
  - 實作情緒分析功能（positive / negative）
  - 根據情緒分析結果選擇不同的回應策略
  - 建立客服系統的基礎架構：正面情緒→鼓勵回應，負面情緒→安撫回應

### demo4-7_gemini_interactive.py: 🎓 AI 學生輔導系統（互動式條件鏈應用）
- **學習重點**：
  - 建立持續互動的 Conditional Chain 系統
  - 使用 Python `input()` 實現即時對話功能
  - 實作多分類困擾類型分析（感情、課業、家庭、人際關係、生涯規劃）
  - 根據不同困擾類型，自動選擇對應的輔導 chain
  - 六個專業輔導 chain：
    * `relationship_counseling_chain` - 感情困擾輔導
    * `academic_counseling_chain` - 課業困擾輔導
    * `family_counseling_chain` - 家庭困擾輔導
    * `interpersonal_counseling_chain` - 人際關係輔導
    * `career_counseling_chain` - 生涯規劃輔導
    * `other_counseling_chain` - 其他困擾輔導
  - 設計友善的使用者介面與錯誤處理機制
- **執行方式**：
  ```bash
  poetry run python demo1/demo4-7_gemini_interactive.py
  ```
- **使用範例**：
  - 「我跟男/女朋友分手了，感覺很難過」（感情困擾）
  - 「最近考試壓力好大，成績一直不理想」（課業困擾）
  - 「爸媽常常吵架，讓我很煩躁」（家庭困擾）

### wife_translator.py: 💑 老婆翻譯機（實用型條件鏈應用）
- **學習重點**：
  - 應用 Conditional Chain 解決實際生活情境
  - 實作語境分析與意圖識別功能
  - 建立五種話語類型分類系統：
    * 表面隨便型 -「都可以」、「隨便」
    * 委託決定型 -「你決定」
    * 暗示期待型 -「你看著辦」
    * 被動配合型 -「我陪你就好」
    * 隱藏在意型 -「沒關係」、「沒意見」
  - 每個話語類型對應專門的翻譯 chain，提供：
    * 真實意圖翻譯（她真正想說的話）
    * 具體回應建議（如何適當回應）
  - 內建範例查看功能（輸入 `example` 查看 10 個常見對話）
  - 展示 Chain 在日常溝通場景的實用價值
- **執行方式**：
  ```bash
  poetry run python demo1/wife_translator.py
  ```
- **使用範例**：
  - 「我吃哪間餐廳都可以。」→ 分析類型 → 提供翻譯與建議
  - 「你決定吧。」→ 識別委託決定型 → 給予決斷力建議
  - 「沒關係，我隨便。」→ 檢測隱藏在意 → 建議主動詢問

## 故障排除

### 問題：找不到 poetry 命令

**解決方法**：
- macOS/Linux: 將 `export PATH="$HOME/.local/bin:$PATH"` 加入 `~/.bashrc` 或 `~/.zshrc`
- Windows: 確認 Poetry 的安裝路徑已加入系統 PATH

### 問題：ModuleNotFoundError

**解決方法**：
```bash
# 確認在正確的目錄（從專案根目錄）
cd python_langchain_gemini_azure/CH4/demo1

# 重新安裝依賴
poetry install
```

### 問題：API Key 錯誤

**解決方法**：
1. 確認 `.env` 檔案位於 CH4/demo1 目錄
2. 確認 API Key 沒有多餘的空格或引號
3. 確認 API Key 仍然有效且有配額
4. 對於 Azure OpenAI，確認所有必要的環境變數都已設定

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

### 問題：LangChain 版本相關錯誤

**解決方法**：
```bash
# 確認使用相容的 LangChain 版本
poetry show langchain langchain-core langchain-community

# 如果版本不相容，重新安裝
poetry install --no-root
```

## 相關資源

- [LangChain 官方文檔](https://python.langchain.com/)
- [LangChain Chains 文檔](https://python.langchain.com/docs/modules/chains/)
- [LangChain Sequential Chains](https://python.langchain.com/docs/how_to/sequence/)
- [Poetry 官方文檔](https://python-poetry.org/docs/)
- [Google Gemini API 文檔](https://ai.google.dev/docs)
- [Azure OpenAI API 文檔](https://learn.microsoft.com/azure/ai-services/openai/)

## 注意事項

- 本專案使用 Poetry 進行依賴管理，建議不要混用 pip
- API Keys 請勿上傳至版本控制系統（`.env` 已在 `.gitignore` 中）
- 使用 API 前請確認服務商的定價和配額限制
- MultiPromptChain 和 Conditional Chain 需要較高的 LLM 推理能力，建議使用較新的模型（如 GPT-4 或 Gemini 1.5）
- 執行 chain 時可以設定 `verbose=True` 來查看每個步驟的執行過程

