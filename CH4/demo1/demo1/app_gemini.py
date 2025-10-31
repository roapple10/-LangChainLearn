from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import dotenv_values
import os

config = dotenv_values(dotenv_path="../../.env")
# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

prompt = PromptTemplate.from_template("Translate the following English text to zh-tw: {text}")

# 初始化語言模型
model = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0.7,
)

# 建 LLMChain
chain = LLMChain(llm=model, prompt=prompt,verbose=True)

# 執行 LLMChain
#result = chain.invoke({"text": "Hello, how are you?"})
#result = chain.run(text="Hello, how are you?")
#result = chain.run({"text": "Hello, how are you?"})
result = chain(inputs={"text": "Hello, how are you?"})
print(result) 


