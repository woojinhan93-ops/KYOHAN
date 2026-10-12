import streamlit as st
from openai import OpenAI

BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "minimaxai/minimax-m3"

st.set_page_config(
    page_title="KYOHAN",
    page_icon="✦",
    layout="centered",
)

st.markdown("""
<style>
.block-container {
    max-width: 760px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}
h1 { letter-spacing: -0.04em; }
div[data-testid="stTextArea"] textarea {
    font-size: 16px;
    line-height: 1.55;
}
.stButton > button {
    height: 3.2rem;
    font-size: 16px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("KYOHAN")
st.caption("아이템을 말하면 KYOHAN의 기준으로 디자인 방향을 제안합니다.")

try:
    NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"]
except Exception:
    st.error("NVIDIA API 키가 설정되지 않았습니다.")
    st.stop()

with st.form("kyohan_design_form"):
    brief = st.text_area(
        "무엇을 만들까?",
        placeholder=(
            "예: 코튼 트윌 팬츠. 스트레이트 핏이고 기장은 길게. "
            "샌들이나 뮬을 신었을 때 바닥에 살짝 닿는 정도. "
            "테이퍼드는 싫고 블랙/화이트로 보고 싶어."
        ),
        height=190,
    )

    reference = st.text_area(
        "추가로 꼭 지킬 것 / 레퍼런스 (선택)",
        placeholder="예: 장식적인 디테일은 빼고, 허리와 힙은 정돈되게.",
        height=100,
    )

    submit = st.form_submit_button(
        "디자인 제안 받기",
        use_container_width=True,
        type="primary",
    )

if submit:
    if not brief.strip():
        st.error("만들고 싶은 옷을 한 줄이라도 적어주세요.")
        st.stop()

    client = OpenAI(base_url=BASE_URL, api_key=NVIDIA_API_KEY)

    system_prompt = """
너는 KYOHAN의 전담 의상 디자이너다.

KYOHAN은 'Adult Uniform'을 지향한다.
옷을 고르는 일이 귀찮은 날에도 자연스럽게 손이 가고,
생각 없이 입어도 사람의 비율과 실루엣이 좋아 보이는 옷을 만든다.

디자인 원칙:
- 실루엣과 비율이 가장 중요하다.
- 힘을 뺀 듯하지만 정돈되어 있어야 한다.
- 불필요한 장식과 과도한 로고는 배제한다.
- 유행을 억지로 좇기보다 오래 손이 가는 표준을 만든다.
- 사용자가 명시한 조건은 임의로 바꾸지 않는다.
- 요청하지 않은 디테일을 억지로 추가하지 않는다.
- 추상적인 미사여구보다 실제 옷을 만들 수 있는 구체적인 언어를 쓴다.
- 기존 브랜드나 디자이너를 참고하더라도 그대로 복제하지 않는다.
- 답변은 한국어로, 짧고 선명하게 쓴다.

반드시 아래 순서로 답한다.

# 한 줄 방향
제품의 핵심을 한 문장으로.

# 실루엣
핏, 기장, 볼륨, 착용했을 때의 비율.

# 핵심 디테일
앞/뒤/소매/포켓/여밈 등 정말 필요한 것만.

# 소재와 컬러
가장 적합한 선택과 이유.

# 반드시 지킬 것
샘플 제작에서 무너지면 안 되는 3~5가지.

# 첫 샘플 체크
실물 샘플을 받았을 때 가장 먼저 볼 3가지.
""".strip()

    user_prompt = f"""
[디자인 요청]
{brief}

[추가 고정 조건 / 레퍼런스]
{reference if reference.strip() else "없음"}

KYOHAN의 기본 철학은 다시 설명하지 말고,
이 아이템을 실제로 어떻게 디자인할지 바로 제안해줘.
""".strip()

    with st.spinner("생각 중..."):
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.65,
                top_p=0.9,
                max_tokens=2200,
            )
            st.markdown("---")
            st.markdown(response.choices[0].message.content)
        except Exception as e:
            st.error("API 호출 중 오류가 발생했습니다.")
            st.code(str(e))
