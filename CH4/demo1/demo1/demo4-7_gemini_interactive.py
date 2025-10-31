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
    temperature=0.5,
)

# 定義困擾類型分析的提示樣板
concern_analysis_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""分析這位學生的困擾類型，並僅回答以下其中一個選項：
- 'relationship'（感情困擾）
- 'academic'（課業困擾）
- 'family'（家庭困擾）
- 'interpersonal'（人際關係困擾）
- 'career'（生涯規劃困擾）
- 'other'（其他困擾）

學生的話：'{student_input}'

請只回答上述分類之一，不要有其他說明。"""
)
# 建立困擾類型分析的 LLMChain
concern_analysis_chain = LLMChain(llm=llm, prompt=concern_analysis_prompt)

# 感情困擾輔導的 PromptTemplate
relationship_counseling_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""你是一位專業且溫暖的學生輔導老師。學生向你傾訴感情上的困擾：

學生的話：'{student_input}'

請以輔導老師的身份給予：
1. 同理與傾聽的回應
2. 具體的建議或觀點
3. 鼓勵與支持

請用溫暖、理解的語氣回應，約100-150字。"""
)
relationship_counseling_chain = LLMChain(llm=llm, prompt=relationship_counseling_prompt)

# 課業困擾輔導的 PromptTemplate
academic_counseling_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""你是一位專業且溫暖的學生輔導老師。學生向你傾訴課業上的困擾：

學生的話：'{student_input}'

請以輔導老師的身份給予：
1. 理解學生的壓力與困難
2. 具體的學習建議或策略
3. 鼓勵與信心的建立

請用溫暖、支持的語氣回應，約50字。"""
)
academic_counseling_chain = LLMChain(llm=llm, prompt=academic_counseling_prompt)

# 家庭困擾輔導的 PromptTemplate
family_counseling_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""你是一位專業且溫暖的學生輔導老師。學生向你傾訴家庭方面的困擾：

學生的話：'{student_input}'

請以輔導老師的身份給予：
1. 同理學生的處境與感受
2. 提供適當的觀點與建議
3. 給予情緒支持與陪伴

請用溫暖、理解的語氣回應，約50字。"""
)
family_counseling_chain = LLMChain(llm=llm, prompt=family_counseling_prompt)

# 人際關係困擾輔導的 PromptTemplate
interpersonal_counseling_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""你是一位專業且溫暖的學生輔導老師。學生向你傾訴人際關係的困擾：

學生的話：'{student_input}'

請以輔導老師的身份給予：
1. 理解學生在人際互動中的困難
2. 提供具體的溝通技巧或建議
3. 鼓勵與支持

請用溫暖、友善的語氣回應，約50字。"""
)
interpersonal_counseling_chain = LLMChain(llm=llm, prompt=interpersonal_counseling_prompt)

# 生涯規劃困擾輔導的 PromptTemplate
career_counseling_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""你是一位專業且溫暖的學生輔導老師。學生向你傾訴生涯規劃的困擾：

學生的話：'{student_input}'

請以輔導老師的身份給予：
1. 理解學生對未來的焦慮與困惑
2. 提供探索自我的方向與建議
3. 給予信心與鼓勵

請用溫暖、啟發的語氣回應，約50字。"""
)
career_counseling_chain = LLMChain(llm=llm, prompt=career_counseling_prompt)

# 其他困擾輔導的 PromptTemplate
other_counseling_prompt = PromptTemplate(
    input_variables=["student_input"],
    template="""你是一位專業且溫暖的學生輔導老師。學生向你傾訴他的困擾：

學生的話：'{student_input}'

請以輔導老師的身份給予：
1. 同理學生的感受
2. 提供適當的建議與觀點
3. 給予支持與鼓勵

請用溫暖、理解的語氣回應，約50字。"""
)
other_counseling_chain = LLMChain(llm=llm, prompt=other_counseling_prompt)


def execute_conditional_chain(student_input):
    """執行條件式 chain，根據困擾類型分析結果選擇對應的輔導回應"""
    # 第一步：使用 LLM 來分析困擾類型
    print("🔍 正在分析困擾類型...")
    concern_result = concern_analysis_chain.run({"student_input": student_input})
    
    # 清理結果，移除引號和空白
    concern_type = concern_result.strip().lower().replace("'", "").replace('"', '')
    
    # 定義困擾類型對應的顯示文字和表情符號
    concern_display = {
        "relationship": "💔 感情困擾",
        "academic": "📚 課業困擾",
        "family": "🏠 家庭困擾",
        "interpersonal": "👥 人際關係困擾",
        "career": "🎯 生涯規劃困擾",
        "other": "💭 其他困擾"
    }
    
    # 顯示困擾類型分析結果
    display_text = concern_display.get(concern_type, "💭 其他困擾")
    print(f"📊 困擾類型分析: {display_text}\n")
    
    # 第二步：根據困擾類型選擇要執行的輔導 chain
    if "relationship" in concern_type:
        # 感情困擾
        return relationship_counseling_chain.invoke({"student_input": student_input})
    elif "academic" in concern_type:
        # 課業困擾
        return academic_counseling_chain.invoke({"student_input": student_input})
    elif "family" in concern_type:
        # 家庭困擾
        return family_counseling_chain.invoke({"student_input": student_input})
    elif "interpersonal" in concern_type:
        # 人際關係困擾
        return interpersonal_counseling_chain.invoke({"student_input": student_input})
    elif "career" in concern_type:
        # 生涯規劃困擾
        return career_counseling_chain.invoke({"student_input": student_input})
    else:
        # 其他困擾
        return other_counseling_chain.invoke({"student_input": student_input})


def main():
    """主要互動循環"""
    print("=" * 70)
    print("🎓 歡迎使用 AI 學生輔導系統")
    print("=" * 70)
    print("💡 這是一個安全、溫暖的傾訴空間")
    print("💡 系統會分析你的困擾類型，並提供專業的輔導建議")
    print()
    print("📋 可以協助的困擾類型：")
    print("   💔 感情困擾")
    print("   📚 課業困擾")
    print("   🏠 家庭困擾")
    print("   👥 人際關係困擾")
    print("   🎯 生涯規劃困擾")
    print()
    print("💡 輸入 'quit', 'exit' 或 'q' 來結束對話")
    print("=" * 70)
    print()
    
    conversation_count = 0
    
    while True:
        try:
            # 接收學生輸入
            student_input = input("🎓 學生：").strip()
            
            # 檢查是否要退出
            if student_input.lower() in ['quit', 'exit', 'q', '退出', '結束']:
                print("\n" + "=" * 70)
                print("👋 感謝你的信任，希望我們的對話對你有幫助。")
                print("💪 記得，你並不孤單，隨時歡迎再來聊聊。")
                print("🌟 祝你一切順利！")
                print("=" * 70)
                break
            
            # 檢查是否為空輸入
            if not student_input:
                print("⚠️  請輸入你想說的話\n")
                continue
            
            print()  # 空行，讓輸出更清晰
            conversation_count += 1
            
            # 執行條件式 chain
            result = execute_conditional_chain(student_input)
            
            # 顯示輔導老師的回應
            print("👨‍🏫 輔導老師：")
            print("-" * 70)
            print(result["text"])
            print("-" * 70)
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 對話已中斷，期待下次再聊！")
            break
        except Exception as e:
            print(f"\n❌ 發生錯誤: {str(e)}")
            print("請再試一次，或者換個方式表達你的困擾。\n")
            continue


if __name__ == "__main__":
    main()

