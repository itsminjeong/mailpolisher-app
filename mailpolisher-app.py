import streamlit as st
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# 환경 변수에서 API 키 불러오기
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 페이지 설정
st.set_page_config(page_title="이메일 작성기", page_icon="📧")
st.title("이메일 작성기")
st.markdown("자유롭게 메일 내용을 입력하면 GPT가 정중하고 자연스럽게 다듬어드려요.")

# 사용자 입력
user_input = st.text_area(
    label="메일 내용을 입력하세요:",
    placeholder="예: 교수님께 휴강 여부를 여쭤보는 메일을 쓰고 싶어요"
)

# 메일 생성 버튼
generate = st.button("📨 메일 생성하기")

# 프롬프트 템플릿 정의
prompt_template = PromptTemplate(
    input_variables=["email"],
    template="""
    아래 내용을 참고하여 정중하고 자연스러운 이메일을 작성해주세요.

    이메일 요지: {email}
    """
)

# GPT 호출 함수 (content만 추출)
def generate_email(email_input):
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.0, api_key=openai_api_key)
    response = llm.invoke(prompt_template.format(email=email_input))
    return response.content.strip()  # content만 반환

# 결과 출력
if user_input.strip():
    with st.spinner("이메일 작성 중..."):
        email_result = generate_email(user_input)
        st.markdown("### ✉️ 완성된 이메일:")
        st.text_area("📄 결과", value=email_result, height=250)
