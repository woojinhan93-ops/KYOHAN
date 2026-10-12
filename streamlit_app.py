import base64
import io

from PIL import Image
import streamlit as st
from openai import OpenAI

BASE_URL = "https://integrate.api.nvidia.com/v1"
MODEL_NAME = "minimaxai/minimax-m3"

KYOHAN_ICON = Image.open(io.BytesIO(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAIAAAAlC+aJAAAEcElEQVR42u2WXUxURxTHz8y9+3H5WvYuluxmA4EoUZbSgMl+WNaFJm20i3wLWrG0bJ9om2irKE3EAoKVpmqFFTSxLQ8KJBVRU1/ASEGtRItNuyxtoWnSpkUkbIlQQpe99/Zh7M0G3Nq1Lz7M72Ez+58zc+acmTtnACgUCoVCoVAoFAqFQqFQKBTKUwRCiGEY0sYYI4RW6qQruM0wDDFYpgf/DR5OJgzuXekCISR7fxKWzS5PKv+GMnvkwH/J12OV8OZKSVnTUF9HFrE+M9PlqlSwLAA4HI4PDjcBAMuyAOB0vmwymcjAdWvXnvj4eHt7W3tbW3a2Q7bJz8srL99BbHieP9RQr1AoZEc6ni8uKgreqGfT0t6rqQEAYma1WjIyMsLICLGz27O8nm+J+w+bm41GI9lrTUzMTxPj28rKACA5Ofn4sWMREREAYDGbvaOe4uJig8Gw0W4fuXO7fMfDRde9f/DkSTdZX2JCgnf0O47j5PAqXt355/wcx6kRQkSxWMySJL3hqiRBvrJ9e0FB/sqz95gANths1672FxUW7quuJop8NG1W62+//hKr0RxqqDelpgIAAnR9aLC0dKs8yZrVqyd+/IHXagGgZv/+w02NRNfpdDevD6nVauKI47imxsZv7o7s3rULAFRKJQBkZWXV1h74eWL8hZwcANhWVrZ586ZQAbChwngw9+B5+0aVSrUhy06SJ4qiIAgsw3x161ZXd/fAwLUjR5pHvV4AiFul43m+r6+PYRhJkhBC4xMT96enM9dn9vdfXVry22y2qqoqjJFOp4uMjBRFESEkimK2w3Hj5o2Ojo5LFy+0ut0BQQCAqKio4eHhwcHByxd7DcaEhYUFBasIme5QHdHRMV/fuf375GR31znijxxZUZIwQidaWnmt9kJvLxEXFxcxQhzHSZLEsiwRo6OiZmdnAUCpVHm9Y11dXZ2dnT3ne/7y+zHGkgQAUFJSnGZKS09PX/VMfN6WXEEQAEAIBAx6w8DAl+2nTvec/1wUBKKHFwBCEFhaKtlayvN8x2efkikQgCRJJIapqSkAICuem5sfHBo6eKBWFEW/3x8IBN5+602fzzcycpfYzM/P+Xy+mRnf1P1pURAYjAGk59LTJ+/d++LKlbHvx+rqG/bu2UNcS5LkX/JjjPdW7/vD52t1u2d8M2EHgDETq9UCwIsvbdLr9adPtbMsi/4pCBhjTazm4Z6IIsZ49zvv8rz2kzNnXK7Ko0c/Kiwo2FnxGjFQKhUcF0H2UKVSRkRGAkIAkJ+ff/bsOY/H4/GMtrS0xMfHb8l1AoBSpVKwClEUWZateL0SJFHH68K+RmM1sWazWb6Mc3Od5LYhCsdxVqtl5b2Wk5PtcrmcTmfwfZCUlJSSkkIUtVptMZtJZSQiKX8AkGYypaauA4C4uDi9Xi9/tYmJCUaj8ckrw38ctrJehuUvlPH/KmdygpfV9ke+CIJfE+RBEeqxILeXbaBcyJblIvghQ6FQKBQKhUKhUCgUCoVCoVCeDv4GjKViuy4XI4sAAAAASUVORK5CYII=")))

st.set_page_config(
    page_title="KYOHAN",
    page_icon=KYOHAN_ICON,
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
:root {
    --kyohan-bg: #F8F8F8;
    --kyohan-text: #111111;
    --kyohan-muted: #6E6E69;
    --kyohan-faint: #969690;
    --kyohan-line: #D8D8D3;
    --kyohan-soft: #EFEFEB;
}

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial,
        "Noto Sans KR", sans-serif;
}

.stApp {
    background: var(--kyohan-bg);
    color: var(--kyohan-text);
}

header[data-testid="stHeader"] {
    display: none;
}

#MainMenu,
footer,
header[data-testid="stHeader"],
div[data-testid="stToolbar"],
div[data-testid="stDecoration"],
div[data-testid="stStatusWidget"],
[data-testid="stAppDeployButton"],
[data-testid="stViewerBadge"],
.stDeployButton,
a[href*="streamlit.io/cloud"] {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    max-width: 760px;
    padding-top: 5rem;
    padding-bottom: 7rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.kyohan-kicker {
    margin: 0 0 1rem 0;
    color: var(--kyohan-faint);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

.kyohan-wordmark {
    margin: 0;
    color: var(--kyohan-text);
    font-size: clamp(3rem, 8vw, 4.9rem);
    font-weight: 520;
    line-height: 0.95;
    letter-spacing: 0.015em;
}

.kyohan-intro {
    max-width: 560px;
    margin: 1.4rem 0 4.5rem 0;
    color: var(--kyohan-muted);
    font-size: 1rem;
    line-height: 1.75;
    word-break: keep-all;
}

.kyohan-section {
    margin: 0 0 1.5rem 0;
    padding-top: 1.15rem;
    border-top: 1px solid var(--kyohan-line);
    color: var(--kyohan-faint);
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
}

.kyohan-note {
    margin-top: 1.2rem;
    color: var(--kyohan-faint);
    font-size: 0.76rem;
    line-height: 1.65;
    word-break: keep-all;
}

div[data-testid="stForm"] {
    border: 0;
    padding: 0;
    background: transparent;
}

div[data-testid="stTextArea"] {
    margin-bottom: 1.3rem;
}

div[data-testid="stTextArea"] label p {
    color: var(--kyohan-text);
    font-size: 0.84rem;
    font-weight: 560;
    letter-spacing: -0.01em;
}

div[data-testid="stTextArea"] textarea {
    border: 1px solid var(--kyohan-line);
    border-radius: 0;
    background: transparent;
    color: var(--kyohan-text);
    box-shadow: none;
    font-size: 0.98rem;
    line-height: 1.7;
    padding: 1rem 1.05rem;
    transition: border-color 140ms ease, background-color 140ms ease;
}

div[data-testid="stTextArea"] textarea::placeholder {
    color: #9A9A94;
    opacity: 1;
}

div[data-testid="stTextArea"] textarea:hover {
    border-color: #B8B8B2;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--kyohan-text) !important;
    box-shadow: none !important;
    background: #FFFFFF;
}

.stButton > button,
div[data-testid="stFormSubmitButton"] > button,
button[kind="primaryFormSubmit"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    min-height: 3rem;
    padding: 0 1.35rem;
    border: 1px solid var(--kyohan-text) !important;
    border-radius: 0 !important;
    background: var(--kyohan-text) !important;
    color: var(--kyohan-bg) !important;
    box-shadow: none !important;
    font-size: 0.84rem;
    font-weight: 600;
    letter-spacing: 0.01em;
    transition: background-color 140ms ease, color 140ms ease;
}

.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover,
button[kind="primaryFormSubmit"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background: var(--kyohan-bg) !important;
    color: var(--kyohan-text) !important;
}

.stButton > button:focus,
div[data-testid="stFormSubmitButton"] > button:focus,
button[kind="primaryFormSubmit"]:focus,
button[data-testid="stBaseButton-primaryFormSubmit"]:focus {
    box-shadow: 0 0 0 2px #BDBDB7 !important;
}

div[data-testid="stAlert"] {
    margin-top: 1.25rem;
    border: 1px solid var(--kyohan-line);
    border-radius: 0;
    background: var(--kyohan-soft);
    color: var(--kyohan-text);
}

div[data-testid="stAlert"] p {
    color: var(--kyohan-text);
}

div[data-testid="stSpinner"] p {
    color: var(--kyohan-muted);
    font-size: 0.84rem;
}

hr {
    margin: 4rem 0 2.1rem 0 !important;
    border: 0 !important;
    border-top: 1px solid var(--kyohan-line) !important;
}

/* AI result typography */
[data-testid="stMarkdownContainer"] h1 {
    margin-top: 2.7rem;
    margin-bottom: 0.8rem;
    color: var(--kyohan-text);
    font-size: 0.86rem;
    font-weight: 650;
    line-height: 1.45;
    letter-spacing: 0.01em;
}

[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 {
    margin-top: 2.2rem;
    margin-bottom: 0.7rem;
    color: var(--kyohan-text);
    font-size: 0.86rem;
    font-weight: 650;
    line-height: 1.45;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #353532;
    font-size: 0.94rem;
    line-height: 1.82;
    word-break: keep-all;
}

[data-testid="stMarkdownContainer"] ul,
[data-testid="stMarkdownContainer"] ol {
    padding-left: 1.25rem;
}

@media (max-width: 700px) {
    .block-container {
        padding-top: 3.2rem;
        padding-bottom: 5rem;
        padding-left: 1.15rem;
        padding-right: 1.15rem;
    }

    .kyohan-intro {
        margin-bottom: 3.4rem;
        font-size: 0.94rem;
    }

    div[data-testid="stFormSubmitButton"] > button,
    button[kind="primaryFormSubmit"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        width: 100%;
    }
}

/* Streamlit version-safe primary action override */
[data-testid="stForm"] button,
form button[kind="primaryFormSubmit"],
button[data-testid="stBaseButton-primaryFormSubmit"] {
    background-color: #111111 !important;
    color: #F8F8F8 !important;
    border: 1px solid #111111 !important;
    border-radius: 0 !important;
    box-shadow: none !important;
}

[data-testid="stForm"] button:hover,
form button[kind="primaryFormSubmit"]:hover,
button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
    background-color: #F8F8F8 !important;
    color: #111111 !important;
}
</style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="kyohan-kicker">Adult Uniform · Design Direction</div>', unsafe_allow_html=True)
st.markdown('<div class="kyohan-wordmark">KYOHAN</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="kyohan-intro">아이템을 입력하면 KYOHAN의 기준으로 실루엣, 비율, 소재와 첫 샘플의 기준을 정리합니다.</div>',
    unsafe_allow_html=True,
)

try:
    NVIDIA_API_KEY = st.secrets["NVIDIA_API_KEY"]
except Exception:
    st.error("현재 디자인 도구를 준비 중입니다. 잠시 후 다시 확인해주세요.")
    st.stop()

st.markdown('<div class="kyohan-section">Product Brief</div>', unsafe_allow_html=True)

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
        "꼭 지킬 조건 / 레퍼런스  ·  선택",
        placeholder="예: 장식적인 디테일은 빼고, 허리와 힙은 정돈되게.",
        height=105,
    )

    submit = st.form_submit_button(
        "디자인 방향 보기",
        type="primary",
    )

st.markdown(
    '<div class="kyohan-note">AI는 제품을 대신 결정하지 않습니다. 입력한 의도와 고정 조건을 바꾸지 않고, KYOHAN의 기준으로 디자인 언어를 정리합니다.</div>',
    unsafe_allow_html=True,
)

if submit:
    if not brief.strip():
        st.error("만들고 싶은 아이템을 한 줄 이상 적어주세요.")
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

    with st.spinner("KYOHAN의 기준으로 정리 중…"):
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
            st.markdown('<div class="kyohan-section">Design Direction</div>', unsafe_allow_html=True)
            st.markdown(response.choices[0].message.content)
        except Exception:
            st.error("디자인 방향을 불러오지 못했습니다. 잠시 후 다시 시도해주세요.")
