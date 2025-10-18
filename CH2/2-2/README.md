# CH2-2: 使用 Google Gemini 進行翻譯

本範例展示如何使用 LangChain 整合 Google Gemini API 來進行文字翻譯。

## 環境需求

- Python 3.8+
- langchain-google-genai
- langchain-core
- python-dotenv

## 安裝套件

### 使用 Poetry（推薦）

```bash
poetry add "langchain-google-genai<3.0.0"
```


## 設定環境變數

1. 在專案目錄下建立 `.env` 檔案
2. 新增以下內容：

```env
GOOGLE_API_KEY=your-google-api-key-here
```

### 如何取得 Google API Key

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入您的 Google 帳號
3. 點擊「Create API Key」
4. 複製生成的 API Key
5. 貼到 `.env` 檔案中

## 執行程式

### 使用 Poetry

```bash
poetry run python app.py
```

### 使用 Python 直接執行

```bash
python app.py
```

## 程式說明

此程式會將中文文言文「知之為知之，不知為不知，是知也。」翻譯成英文。

### 程式架構

1. **載入環境變數** - 使用 `dotenv` 載入 API Key
2. **初始化模型** - 建立 `ChatGoogleGenerativeAI` 實例
3. **建立訊息鏈** - 使用 LangChain 的 LCEL (LangChain Expression Language)
4. **執行翻譯** - 透過 `chain.invoke()` 執行翻譯任務

### 可用的 Gemini 模型

- `gemini-2.5-flash` - 最新快速模型（推薦）
- `gemini-flash-latest` - 自動使用最新 flash 版本
- `gemini-2.5-pro` - 更強大但較慢的模型
- `gemini-pro-latest` - 自動使用最新 pro 版本

### 調整參數

您可以在初始化模型時調整以下參數：

```python
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,  # 0.0-1.0，越高越有創意
    max_output_tokens=1000,  # 最大輸出長度
)
```

## 預期輸出

```
To know is to know; not to know is not to know. This is knowledge.
```

或類似的英文翻譯。

## 進階功能

### 串流輸出

如果想要即時看到生成的內容，可以使用串流模式：

```python
for chunk in model.stream(messages):
    print(chunk.content, end="", flush=True)
```

### 多模態輸入

Gemini 也支援圖片輸入：

```python
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content=[
        {"type": "text", "text": "這張圖片裡有什麼？"},
        {"type": "image_url", "image_url": "https://example.com/image.jpg"}
    ]
)
response = model.invoke([message])
```

## 故障排除

### 錯誤：API Key 無效

確認您的 `.env` 檔案格式正確，且 API Key 沒有多餘的空格或引號。

### 錯誤：模組找不到

確認已正確安裝所有依賴套件：

```bash
poetry install
# 或
pip install -r requirements.txt
```

### 錯誤：配額限制

Google Gemini API 有免費配額限制，如果超過需要等待或升級至付費方案。

## 參考資源

- [LangChain Google GenAI 文件](https://github.com/langchain-ai/langchain-google)
- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API 文件](https://ai.google.dev/docs)

