
import streamlit as st
from groq import Groq

# -------------------- PAGE CONFIGURATION --------------------

st.set_page_config(
    page_title="Muse - The Poetic Chatbot",
    page_icon="✒️",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# -------------------- CUSTOM CSS --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Caveat:wght@500&display=swap');

/* Main page */
.stApp {
    background-color: #f4efe4;
    color: #1a1a1a;
}

/* Remove default top header background */
header[data-testid="stHeader"] {
    background-color: transparent;
}

/* Hide Streamlit's default toolbar decoration */
[data-testid="stToolbar"] {
    right: 1rem;
}

/* Main content width and spacing */
.block-container {
    max-width: 720px !important;
    padding-top: 125px !important;
    padding-bottom: 110px !important;
}

/* ---------------- FIXED MUSE HEADER ---------------- */

/*
   The header is fixed to the browser viewport.
   It stays visible even when the conversation scrolls.
*/

.fixed-muse-header {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100% !important;
    height: 100px !important;

    background-color: #f4efe4 !important;

    z-index: 999999 !important;

    border-bottom: 1px solid #ded6c6;

    display: flex;
    align-items: center;

    box-sizing: border-box;
}

/* Header content */
.fixed-muse-inner {
    width: 100%;
    max-width: 720px;

    margin: 0 auto;
    padding: 0 20px;

    box-sizing: border-box;
}

/* Brand row */
.muse-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Pen icon */
.muse-icon {
    font-size: 2rem;
    line-height: 1;
}

/* Muse name */
.muse-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.3rem;
    font-weight: 600;

    color: #1a1a1a;
    line-height: 1.1;
}

/* Tagline */
.muse-tagline {
    font-family: 'Caveat', cursive;
    font-size: 1.1rem;

    color: #6b6558;

    margin-top: 4px;
    margin-left: 4px;
}

/* ---------------- CHAT MESSAGES ---------------- */

/* Chat message containers */
[data-testid="stChatMessage"] {
    background-color: transparent;
    border-radius: 2px;
    padding: 4px 0;
}

/* User message bubble */
.user-bubble {
    background-color: #e8e1d0;

    border-radius: 8px;
    padding: 10px 14px;

    display: inline-block;

    color: #1a1a1a;

    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;

    line-height: 1.5;

    overflow-wrap: anywhere;
}

/* Muse's poem */
.poem-text {
    font-family: 'Cormorant Garamond', serif;

    font-size: 1.4rem;
    font-style: italic;
    line-height: 1.7;

    color: #1a1a1a;

    border-left: 2px solid #1a1a1a;
    padding-left: 14px;

    white-space: pre-wrap;
    overflow-wrap: anywhere;
}

/* ---------------- CHAT INPUT ---------------- */

.stChatInput {
    background-color: #f4efe4 !important;
}

.stChatInput textarea {
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic;

    background-color: #fffdf8 !important;
    color: #1a1a1a !important;
}

/* ---------------- MOBILE RESPONSIVENESS ---------------- */

@media (max-width: 768px) {

    .fixed-muse-header {
        height: 90px !important;
    }

    .fixed-muse-inner {
        padding: 0 16px;
    }

    .muse-name {
        font-size: 2rem;
    }

    .muse-icon {
        font-size: 1.8rem;
    }

    .muse-tagline {
        font-size: 1rem;
    }

    .block-container {
        padding-top: 110px !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        padding-bottom: 100px !important;
    }

    .poem-text {
        font-size: 1.25rem;
    }
}
</style>
""", unsafe_allow_html=True)


# -------------------- FIXED MUSE HEADER --------------------

st.markdown("""
<div class="fixed-muse-header">
    <div class="fixed-muse-inner">

        <div class="muse-brand">
            <span class="muse-icon">✒️</span>
            <span class="muse-name">Muse</span>
        </div>

        <div class="muse-tagline">
            turn thoughts into poetry
        </div>

    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- GROQ CLIENT --------------------

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)


# -------------------- MUSE PERSONALITY --------------------

MUSE_PERSONA_PROMPT = """
You are Muse, a gentle and thoughtful poet-companion.

You never speak in plain prose. Every reply you give
must be a short original poem responding to what the
user said.

Rules:
- Reply ONLY with the poem.
- No greetings, no explanations, no "Here is a poem".
- Keep it to 2-4 short lines.
- Match the emotional tone of the message.
- Happy -> bright imagery.
- Sad -> soft imagery.
- Angry -> stormy but never cruel imagery.
"""


# -------------------- CHAT HISTORY --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------- DISPLAY CHAT HISTORY --------------------

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message("user", avatar="🧑"):

            st.markdown(
                f'<div class="user-bubble">'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True
            )

    else:

        with st.chat_message("assistant", avatar="✒️"):

            st.markdown(
                f'<div class="poem-text">'
                f'{msg["content"]}'
                f'</div>',
                unsafe_allow_html=True
            )


# -------------------- CHAT INPUT --------------------

user_input = st.chat_input(
    "Tell Muse what's on your mind..."
)


# -------------------- GENERATE POEM --------------------

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message
    with st.chat_message("user", avatar="🧑"):

        st.markdown(
            f'<div class="user-bubble">'
            f'{user_input}'
            f'</div>',
            unsafe_allow_html=True
        )

    # Generate Muse's reply
    with st.chat_message("assistant", avatar="✒️"):

        placeholder = st.empty()
        full_response = ""

        try:

            stream = client.chat.completions.create(
                model="openai/gpt-oss-20b",

                messages=[
                    {
                        "role": "system",
                        "content": MUSE_PERSONA_PROMPT
                    }
                ] + [
                    {
                        "role": m["role"],
                        "content": m["content"]
                    }
                    for m in st.session_state.messages
                ],

                stream=True,
            )

            # Stream the response word by word
            for chunk in stream:

                delta = chunk.choices[0].delta.content or ""

                full_response += delta

                placeholder.markdown(
                    f'<div class="poem-text">'
                    f'{full_response}▌'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Display final poem without cursor
            placeholder.markdown(
                f'<div class="poem-text">'
                f'{full_response}'
                f'</div>',
                unsafe_allow_html=True
            )

        except Exception:

            full_response = (
                "The muse grows quiet, spent and still,\n"
                "Give me a moment, then speak your will."
            )

            placeholder.markdown(
                f'<div class="poem-text">'
                f'{full_response}'
                f'</div>',
                unsafe_allow_html=True
            )

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
