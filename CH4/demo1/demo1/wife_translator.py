# 老婆翻譯機 - 使用 LangChain 的 Chain 概念
# 引入Chain模組
from langchain.chains import LLMChain

# 引入Google Gemini模組
from langchain_google_genai import ChatGoogleGenerativeAI

# 引入prompt模組
from langchain_core.prompts import PromptTemplate

import os
from dotenv import dotenv_values

config = dotenv_values(dotenv_path="../../.env")

# 設定 Google API Key
os.environ["GOOGLE_API_KEY"] = config.get("GOOGLE_API_KEY")
os.environ["GEMINI_MODEL_ID"] = config.get("GEMINI_MODEL_ID")

llm = ChatGoogleGenerativeAI(
    model=os.environ["GEMINI_MODEL_ID"],
    temperature=0.7,
)

# 定義話語類型分析的提示樣板
speech_analysis_prompt = PromptTemplate(
    input_variables=["wife_speech"],
    template="""分析以下這句話的類型，並僅回答以下其中一個選項：
- 'indifferent'（表面隨便型）
- 'delegate'（委託決定型）
- 'hint'（暗示期待型）
- 'passive'（被動配合型）
- 'concern'（隱藏在意型）

老婆說：'{wife_speech}'

請只回答上述分類之一，不要有其他說明。"""
)
speech_analysis_chain = LLMChain(llm=llm, prompt=speech_analysis_prompt)

# 表面隨便型的翻譯 Chain
indifferent_translation_prompt = PromptTemplate(
    input_variables=["wife_speech"],
    template="""你是一個「老婆翻譯機」，專門翻譯老婆的真實想法。

老婆說：'{wife_speech}'

這是「表面隨便型」的話語。通常老婆說「都可以」、「隨便」時，其實心裡已經有想法了。

請提供：
1. 💭 翻譯（她真正想說的話，30字內）
2. 💡 建議（如何回應，40字內）

格式範例：
💭 翻譯：我其實有想吃那間 X 餐廳，只是不想一直提。
💡 建議：可以說「那我們去你上次提到的那間餐廳好嗎？」主動提起她之前的偏好。"""
)
indifferent_translation_chain = LLMChain(llm=llm, prompt=indifferent_translation_prompt)

# 委託決定型的翻譯 Chain
delegate_translation_prompt = PromptTemplate(
    input_variables=["wife_speech"],
    template="""你是一個「老婆翻譯機」，專門翻譯老婆的真實想法。

老婆說：'{wife_speech}'

這是「委託決定型」的話語。當老婆說「你決定」時，其實是希望你快點決定或怕你不喜歡她的選擇。

請提供：
1. 💭 翻譯（她真正想說的話，30字內）
2. 💡 建議（如何回應，40字內）

格式範例：
💭 翻譯：你快決定，不然我會猶豫很久／我怕你不喜歡我選的。
💡 建議：展現決斷力，但也詢問她的意見「那我們去 A 餐廳，你覺得呢？」"""
)
delegate_translation_chain = LLMChain(llm=llm, prompt=delegate_translation_prompt)

# 暗示期待型的翻譯 Chain
hint_translation_prompt = PromptTemplate(
    input_variables=["wife_speech"],
    template="""你是一個「老婆翻譯機」，專門翻譯老婆的真實想法。

老婆說：'{wife_speech}'

這是「暗示期待型」的話語。老婆希望你能察覺她的期待，提出讓雙方都滿意的選擇。

請提供：
1. 💭 翻譯（她真正想說的話，30字內）
2. 💡 建議（如何回應，40字內）

格式範例：
💭 翻譯：我希望你提個我們倆都會喜歡的選擇。
💡 建議：提出包含她喜好的選項「我們去那間環境不錯又有你愛吃的料理的餐廳？」"""
)
hint_translation_chain = LLMChain(llm=llm, prompt=hint_translation_prompt)

# 被動配合型的翻譯 Chain
passive_translation_prompt = PromptTemplate(
    input_variables=["wife_speech"],
    template="""你是一個「老婆翻譯機」，專門翻譯老婆的真實想法。

老婆說：'{wife_speech}'

這是「被動配合型」的話語。老婆願意配合，但也希望你有主見，帶她去好的地方。

請提供：
1. 💭 翻譯（她真正想說的話，30字內）
2. 💡 建議（如何回應，40字內）

格式範例：
💭 翻譯：我希望你有主見，你帶我去你認為好的地方。
💡 建議：展現自信「那就去我最近發現的一間很棒的店，相信你會喜歡！」"""
)
passive_translation_chain = LLMChain(llm=llm, prompt=passive_translation_prompt)

# 隱藏在意型的翻譯 Chain
concern_translation_prompt = PromptTemplate(
    input_variables=["wife_speech"],
    template="""你是一個「老婆翻譯機」，專門翻譯老婆的真實想法。

老婆說：'{wife_speech}'

這是「隱藏在意型」的話語。老婆說「沒意見」或「沒關係」時，其實心裡是有在意的。

請提供：
1. 💭 翻譯（她真正想說的話，30字內）
2. 💡 建議（如何回應，40字內）

格式範例：
💭 翻譯：我其實有意見，只是不想讓你感覺壓力／需要你主動察覺。
💡 建議：溫柔詢問「我看你好像有點想法，跟我說說你的想法好嗎？」"""
)
concern_translation_chain = LLMChain(llm=llm, prompt=concern_translation_prompt)


def translate_wife_speech(wife_speech):
    """執行老婆翻譯機，根據話語類型提供翻譯和建議"""
    # 第一步：使用 LLM 來分析話語類型
    print("🔍 正在分析話語類型...")
    speech_result = speech_analysis_chain.run({"wife_speech": wife_speech})
    
    # 清理結果
    speech_type = speech_result.strip().lower().replace("'", "").replace('"', '')
    
    # 定義話語類型對應的顯示文字
    speech_display = {
        "indifferent": "😊 表面隨便型",
        "delegate": "🤔 委託決定型",
        "hint": "💝 暗示期待型",
        "passive": "🌸 被動配合型",
        "concern": "😌 隱藏在意型"
    }
    
    # 顯示話語類型分析結果
    display_text = speech_display.get(speech_type, "😊 表面隨便型")
    print(f"📊 話語類型: {display_text}\n")
    
    # 第二步：根據話語類型選擇對應的翻譯 chain
    if "indifferent" in speech_type:
        return indifferent_translation_chain.invoke({"wife_speech": wife_speech})
    elif "delegate" in speech_type:
        return delegate_translation_chain.invoke({"wife_speech": wife_speech})
    elif "hint" in speech_type:
        return hint_translation_chain.invoke({"wife_speech": wife_speech})
    elif "passive" in speech_type:
        return passive_translation_chain.invoke({"wife_speech": wife_speech})
    elif "concern" in speech_type:
        return concern_translation_chain.invoke({"wife_speech": wife_speech})
    else:
        # 預設使用表面隨便型
        return indifferent_translation_chain.invoke({"wife_speech": wife_speech})


def show_examples():
    """顯示範例對話"""
    examples = [
        "我吃哪間餐廳都可以。",
        "你決定吧。",
        "沒關係，我隨便。",
        "你看你覺得好就好。",
        "那隨你。",
        "你想去哪我都可以陪你。",
        "沒什麼好說的。",
        "我沒意見。",
        "你自己決定就好了。",
        "如果你喜歡就好。"
    ]
    
    print("\n💡 常見老婆話語範例：")
    print("-" * 70)
    for i, example in enumerate(examples, 1):
        print(f"{i:2d}. {example}")
    print("-" * 70)
    print()


def main():
    """主要互動循環"""
    print("=" * 70)
    print("💑 老婆翻譯機 - 理解她說的每一句話")
    print("=" * 70)
    print("💭 當老婆說「都可以」、「隨便」時，她真正的意思是什麼？")
    print("💡 這個系統會幫你翻譯並提供回應建議！")
    print()
    print("📋 可以分析的話語類型：")
    print("   😊 表面隨便型 - 「都可以」、「隨便」")
    print("   🤔 委託決定型 - 「你決定」")
    print("   💝 暗示期待型 - 「你看著辦」")
    print("   🌸 被動配合型 - 「我陪你就好」")
    print("   😌 隱藏在意型 - 「沒關係」、「沒意見」")
    print()
    print("💡 輸入 'example' 查看範例")
    print("💡 輸入 'quit', 'exit' 或 'q' 來結束")
    print("=" * 70)
    print()
    
    while True:
        try:
            # 接收輸入
            wife_speech = input("💬 老婆說：").strip()
            
            # 檢查特殊指令
            if wife_speech.lower() in ['quit', 'exit', 'q', '退出', '結束']:
                print("\n" + "=" * 70)
                print("👋 感謝使用老婆翻譯機！")
                print("💝 願你們的溝通越來越順暢！")
                print("=" * 70)
                break
            
            if wife_speech.lower() in ['example', 'examples', '範例']:
                show_examples()
                continue
            
            # 檢查是否為空輸入
            if not wife_speech:
                print("⚠️  請輸入老婆說的話\n")
                continue
            
            print()
            
            # 執行翻譯
            result = translate_wife_speech(wife_speech)
            
            # 顯示翻譯結果
            print("🔮 翻譯結果：")
            print("=" * 70)
            print(result["text"])
            print("=" * 70)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 程式已中斷，再見！")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤: {str(e)}")
            print("請再試一次。\n")
            continue


if __name__ == "__main__":
    main()

