# 這個程式展示如何將 SemanticSimilarityExampleSelector 整合到 FewShotChatMessagePromptTemplate
# 使用 Google Gemini 模型和 GoogleGenerativeAIEmbeddings
# https://developers.googleblog.com/en/gemini-embedding-available-gemini-api/
# https://python.langchain.com/api_reference/google_genai/embeddings/langchain_google_genai.embeddings.GoogleGenerativeAIEmbeddings.html

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import dotenv_values
import os

config = dotenv_values(dotenv_path="../.env")  # dotenv_path="../.env"：指定 .env 的路徑為目前工作目錄的上一層的 .env 檔。

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

model = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],  # 可選: gemini-1.5-flash-latest, gemini-1.5-pro-latest
    temperature=0.7,
)

from langchain_core.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate

example_prompt = HumanMessagePromptTemplate.from_template(
    "{description}"
) + AIMessagePromptTemplate.from_template("{classification}")

examples = [
    {
        "description": "食物偏甜",
        "classification": "南部人",
    },
    {
        "description": "食物偏鹹",
        "classification": "北部人",
    },
    {
        "description": "滷肉飯",
        "classification": "北部人",
    },
    {
        "description": "肉燥飯",
        "classification": "南部人",
    },
    {
        "description": "搭乘大眾運輸，不怕走路",
        "classification": "北部人",
    },
    {
        "description": "騎摩托車，不待轉",
        "classification": "南部人",
    },
    {
        "description": "講話婉轉，不直接",
        "classification": "北部人",
    },
    {
        "description": "講話直接",
        "classification": "南部人",
    },
]


from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate

few_shot_prompt = FewShotChatMessagePromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
)

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

from langchain_core.prompts.chat import ChatPromptTemplate

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "請根據以下描述，判斷是哪一種人："),
        few_shot_prompt,
        ("human", "{input}"),
    ]
)


chain = final_prompt | model | parser

user_input = "醬油喜歡有甜味"
# user_input = "熱情大方，講話直接"
response = chain.invoke({"input": user_input})
print("描述：", user_input)
print("分類：", response)


from langchain_chroma import Chroma
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_google_genai import GoogleGenerativeAIEmbeddings

embedding_function = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.environ["GOOGLE_API_KEY"],
)


example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embedding_function,
    Chroma,
    k=1,
)

# find the most similar example
question = "騎機車經過十字路口會直接左轉"
# question = "喜歡醬油有甜味"
selected_examples = example_selector.select_examples({"description": question})

print(question)
print("最相似的例子是 :")
for example in selected_examples:
    for key, value in example.items():
        print(f"{key}: {value}")
    print("\n")


# Add the selected example to the few-shot prompt

few_shot_prompt_v2 = FewShotChatMessagePromptTemplate(
    # examples=examples,
    example_prompt=example_prompt,
    example_selector=example_selector,
)

print(few_shot_prompt_v2.invoke({"description": "喜歡吃甜甜"}))

from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

from langchain_core.prompts.chat import ChatPromptTemplate

final_prompt_v2 = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                    請根據以下精選的參考描述，判斷是北部人還是南部人，
                    只要回答是「北部人」或「南部人」即可，不用解釋：
                    """,
        ),
        few_shot_prompt_v2,
        ("human", "{input}"),
    ]
)


chain_v2 = final_prompt_v2 | model | parser


user_input = "醬油喜歡有甜味"
# user_input = "熱情大方，講話直接"
response = chain_v2.invoke({"input": user_input})
print("描述：", user_input)
print("分類：", response)

