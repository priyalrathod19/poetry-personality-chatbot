import streamlit as st
from groq import Groq

st.set_page_config(page_title="Muse - The Poetic Chatbot", page_icon="\u2712\ufe0f", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Caveat:wght@500&display=swap');

.stApp {
    background-color: #f4efe4;
    color: #1a1a1a;
}

h1 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

.subtitle {
    font-family: 'Caveat', cursive;
    font-size: 1.3rem;
    color: #6b6558;
    margin-top: -12px;
}

[data-testid="stChatMessage"] {
    background-color: transparent;
    border-radius: 2px;
    padding: 4px 0;
}

.user-bubble {
    background-color: #e8e1d0;
    border-radius: 2px;
    padding: 8px 14px;
    display: inline-block;
    color: #1a1a1a;
}

.poem-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.4rem;
    font-style: italic;
    line-height: 1.7;
    color: #1a1a1a;
    border-left: 2px solid #1a1a1a;
    padding-left: 14px;
}

textarea, input {
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

st.title("\u2712\ufe0f Muse")
st.markdown('<p class="subtitle">turn thoughts into poetry</p>', unsafe_allow_html=True)

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

MUSE_PERSONA_PROMPT = """
You are Muse, a gentle and thoughtful poet-companion. You never speak in plain
prose. Every reply you give must be a short original poem responding to what
the user said.

Rules:
- Reply ONLY with the poem. No greetings, no explanations, no "Here is a poem".
- Keep it to 2-4 short lines.
- Match the emotional tone of the message (happy -> bright imagery, sad -> soft
  imagery, angry -> stormy but never cruel imagery).
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="\U0001F9D1"):
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="\u2712\ufe0f"):
            st.markdown(f'<div class="poem-text">{msg["content"]}</div>', unsafe_allow_html=True)

user_input = st.chat_input("Tell Muse what's on your mind...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="\U0001F9D1"):
        st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="\u2712\ufe0f"):
        placeholder = st.empty()
        full_response = ""
        try:
            stream = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[{"role": "system", "content": MUSE_PERSONA_PROMPT}] +
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                full_response += delta
                placeholder.markdown(f'<div class="poem-text">{full_response}\u258c</div>', unsafe_allow_html=True)
            placeholder.markdown(f'<div class="poem-text">{full_response}</div>', unsafe_allow_html=True)
        except Exception:
            full_response = "The muse grows quiet, spent and still,\nGive me a moment, then speak your will."
            placeholder.markdown(f'<div class="poem-text">{full_response}</div>', unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
