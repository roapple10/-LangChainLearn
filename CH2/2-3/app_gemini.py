from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import dotenv_values

config = dotenv_values(dotenv_path="../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

model = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],  # 可選: gemini-flash-latest, gemini-2.5-pro
    temperature=0.7,
)

# exp1
parser = StrOutputParser()
chain = model | parser
# model.invoke("你好").content
result1 = chain.invoke("你好")
print("=== Exp1 結果 ===")
print(result1)
print()

# exp2
parser = StrOutputParser()
chain = model | parser
# model.invoke("你好").content
result2 = chain.invoke("將以下的內容翻譯為英文：知之為知之，不知為不知，是知也。")
print("=== Exp2 結果 ===")
print(result2)
print()

# exp3
prompt_template = ChatPromptTemplate.from_messages(
    [("system", "將以下的內容翻譯為{language}"), ("user", "{text}")]
)

chain = prompt_template | model | parser

target_language = "日文"
user_input = "知之為知之，不知為不知，是知也。"
result3 = chain.invoke({"language": target_language, "text": user_input})
print("=== Exp3 結果 ===")
print(result3)
