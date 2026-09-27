import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

st.set_page_config(
    page_title="Ali ChatBot",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Design system
#   Background : #12151C  (deep ink navy, not flat black)
#   Surface    : #191D26  (panels / sidebar)
#   Hairline   : #262B36
#   Text       : #EDEEF2  (primary)  /  #8A8F9C (muted)
#   Accent     : #E8963C  (warm amber — signals "assistant / active")
#   User tint  : #232A3A  (cool slate — signals "you")
#   Display type : "Fraunces"  (serif, has personality, used only for the
#                  wordmark and the empty-state headline)
#   UI type      : "IBM Plex Sans" (body) + "IBM Plex Mono" (small technical
#                  labels — model name, status — used sparingly, on purpose)
# ---------------------------------------------------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .stApp {
        background: #12151C;
        color: #EDEEF2;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* ---------------- Sidebar ---------------- */
    [data-testid="stSidebar"] {
        background: #191D26;
        border-right: 1px solid #262B36;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 34px 24px;
    }

    .wordmark {
        font-family: 'Fraunces', serif;
        font-size: 26px;
        font-weight: 600;
        color: #EDEEF2;
        display: flex;
        align-items: baseline;
        gap: 9px;
        margin-bottom: 6px;
    }
    .wordmark .mark {
        color: #E8963C;
        font-size: 15px;
    }

    .side-caption {
        font-size: 13px;
        line-height: 1.6;
        color: #8A8F9C;
        margin-bottom: 28px;
        padding-bottom: 24px;
        border-bottom: 1px solid #262B36;
    }

    .side-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 10.5px;
        letter-spacing: 0.04em;
        color: #5C6272;
        margin: 22px 0 12px 0;
    }

    .meta-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 0;
        font-size: 13.5px;
    }
    .meta-row .k { color: #8A8F9C; }
    .meta-row .v {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 12px;
        color: #C7CAD3;
    }

    .status-line {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #7FBF8F;
        margin-top: 20px;
    }
    .status-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #7FBF8F;
        box-shadow: 0 0 0 3px rgba(127, 191, 143, 0.15);
    }

    div[data-testid="stSidebar"] button {
        background: transparent !important;
        color: #EDEEF2 !important;
        border: 1px solid #333A4A !important;
        border-radius: 8px !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        transition: border-color 0.15s ease, color 0.15s ease;
    }
    div[data-testid="stSidebar"] button:hover {
        border-color: #E8963C !important;
        color: #E8963C !important;
    }

    /* ---------------- Main column ---------------- */
    .main-wrap {
        max-width: 760px;
        margin: 0 auto;
        padding: 8px 20px 140px 20px;
    }

    .empty-state {
        padding: 90px 0 40px 0;
    }
    .empty-state .headline {
        font-family: 'Fraunces', serif;
        font-size: 34px;
        font-weight: 500;
        color: #EDEEF2;
        margin-bottom: 10px;
    }
    .empty-state .sub {
        font-size: 15px;
        color: #8A8F9C;
        max-width: 480px;
        line-height: 1.6;
    }

    /* ---------------- Chat messages ---------------- */
    [data-testid="stChatMessage"] {
        background: transparent;
        border: none;
        padding: 14px 0;
        margin-bottom: 2px;
    }

    /* user message: right-aligned tinted bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        display: flex;
        justify-content: flex-end;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
        background: #232A3A;
        border-radius: 14px 14px 2px 14px;
        padding: 12px 16px;
        max-width: 78%;
        color: #EDEEF2;
    }
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageAvatarUser"] {
        display: none;
    }

    /* assistant message: left rule instead of a boxed card */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stChatMessageContent"] {
        border-left: 2px solid #E8963C;
        padding: 2px 0 2px 16px;
        max-width: 92%;
    }
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"],
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] p,
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] li,
    [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] span {
        font-size: 15.5px;
        line-height: 1.65;
        color: #F5F6FA !important;
    }

    /* ---------------- Chat input ---------------- */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInputContainer"],
    [data-testid="stBottomBlockContainer"] [data-baseweb="textarea"],
    [data-testid="stBottomBlockContainer"] [data-baseweb="base-input"] {
        background: #191D26 !important;
        border-color: #333A4A !important;
        border-radius: 12px !important;
    }
    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInput"] textarea:active {
        font-size: 15px !important;
        color: #F5F6FA !important;
        background-color: transparent !important;
        -webkit-text-fill-color: #F5F6FA !important;
        caret-color: #F5F6FA !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #6B7180 !important;
        opacity: 1 !important;
    }
    [data-testid="stChatInputSubmitButton"] {
        background-color: #E8963C !important;
        border-color: #E8963C !important;
    }
    [data-testid="stChatInputSubmitButton"] svg {
        fill: #12151C !important;
        color: #12151C !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful assistant.")
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_resource
def get_model():
    return ChatGroq(model="openai/gpt-oss-120b")


model = get_model()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        "<div class='wordmark'>Ali <span class='mark'>◆</span> ChatBot</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='side-caption'>A conversational assistant </div>",
        unsafe_allow_html=True
    )

    if st.button("New conversation", use_container_width=True):
        st.session_state.messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("<div class='side-label'>SYSTEM</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='meta-row'><span class='k'>Model</span>"
        "<span class='v'>gpt-oss-120b</span></div>"
        "<div class='meta-row'><span class='k'>Provider</span>"
        "<span class='v'>Groq</span></div>"
        "<div class='meta-row'><span class='k'>Framework</span>"
        "<span class='v'>LangChain</span></div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='status-line'><span class='status-dot'></span>"
        "Online</div>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------------
# Main chat area
# ---------------------------------------------------------------------------
st.markdown("<div class='main-wrap'>", unsafe_allow_html=True)

if len(st.session_state.chat_history) == 0:
    st.markdown(
        "<div class='empty-state'>"
        "<div class='headline'>What can I help with?</div>"
        "<div class='sub'>Ask a question, work through a problem, "
        "or just start typing below.</div>"
        "</div>",
        unsafe_allow_html=True
    )

for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

prompt = st.chat_input("Message Ali ChatBot…")

if prompt:
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            response = model.invoke(st.session_state.messages)
        st.markdown(response.content)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response.content}
    )

st.markdown("</div>", unsafe_allow_html=True)