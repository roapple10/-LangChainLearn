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

parser = StrOutputParser()

system_prompt = """
請按照這個格式回答：
單字：{text}
情境：{scenario}
{native_language}翻譯： 
{target_language}造句：
{native_language}翻譯：
"""

prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{text}")]
)

chain = prompt_template | model | parser

native_language = "繁體中文"
target_language = "英文"
scenario_array = [
    "在餐廳",
    "在學校",
    "在家裡",
    "在辦公室",
    "在機場",
]
vocabularies = [
    "hungry",
    "glad",
    "stranger",
    "proud",
    "excited",
]

results = []

for vocabulary in vocabularies:
    for scenario in scenario_array:
        result = chain.invoke(
            {
                "native_language": native_language,
                "scenario": scenario,
                "target_language": target_language,
                "text": vocabulary,
            }
        )
        results.append(result)

for result in results:
    print(result)
    print("=====")
