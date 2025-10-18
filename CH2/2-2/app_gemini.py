from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import dotenv_values

# 載入環境變數
config = dotenv_values(dotenv_path="../.env") 	#dotenv_path="../.env"：指定 .env 的路徑為目前工作目錄的上一層的 .env 檔。

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

# 初始化 Google Gemini 模型
model = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],  # 可選: gemini-flash-latest, gemini-2.5-pro
    temperature=0.7,
)

# 建立輸出解析器
parser = StrOutputParser()
chain = model | parser

# 測試輸入
user_input = "知之為知之，不知為不知，是知也。"

# 建立訊息
messages = [
    SystemMessage(content="將以下的內容翻譯為英文。"),
    HumanMessage(content=user_input),
]

# 執行鏈並輸出結果
result = chain.invoke(messages)
print(result)

