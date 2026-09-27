import streamlit as st
from groq import Groq
from html import escape

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

html, body, [class*="css"] {
    font-family: 'Cormorant Garamond', serif;
}

.stApp {
    background-color: #f4efe4;
    color: #1a1a1a;
}

/* Hide Streamlit header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main content */
.block-container {
    max-width: 720px !important;
    padding-top: 125px !important;
    padding-bottom: 120px !important;
}

/* Fixed header */
.fixed-muse-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100px;

    background-color: #f4efe4;

    border-bottom: 1px solid #ded6c6;

    z-index: 999999;

    display: flex;
    align-items: center;

    box-sizing: border-box;
}

/* Header inner content */
.fixed-muse-inner {
    width: 100%;
    max-width: 720px;
    margin: 0 auto;
    padding: 0 20px;
    box-sizing: border-box;
}

/* Muse brand */
.muse-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Pen */
.muse-icon {
    font-size: 2rem;
    line-height: 1;
}

/* Muse */
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

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: transparent !important;
    padding: 6px 0 !important;
}

/* User bubble */
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

/* Poem */
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

/* Chat input */
.stChatInput {
    background-color: #f4efe4 !important;
}

.stChatInput textarea {
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic !important;

    background-color: #fffdf8 !important;
    color: #1a1a1a !important;
}

.stChatInput textarea::placeholder {
    color: #6b6558 !important;
    opacity: 1 !important;
}

/* Mobile */
@media (max-width: 768px) {

    .fixed-muse-header {
        height: 90px;
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
        padding-bottom: 105px !important;
    }

    .poem-text {
        font-size: 1.25rem;
    }

    .user-bubble {
        font-size: 1.1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# -------------------- FIXED MUSE HEADER --------------------

st.html("""
<div class="fixed-muse-header">
    <div class="fixed-muse-inner">
        <div class="muse-brand">
            <span class="muse-icon">✒️</span>
            <span class="muse-name">Muse</span>
        </div>
        <div class="muse-tagline">turn thoughts into poetry</div>
    </div>
</div>
""")


# -------------------- GROQ CLIENT --------------------

try:
    client = Groq(
        api_key=st.secrets["GROQ_API_KEY"]
    )
except Exception:
    st.error("GROQ_API_KEY is missing. Please add it to Streamlit Secrets.")
    st.stop()


# -------------------- MUSE PERSONALITY --------------------

MUSE_PERSONA_PROMPT = """
You are Muse, a gentle and thoughtful poet-companion.

You never speak in plain prose.

Every reply must be a short original poem responding
directly to what the user said.

Rules:

- Reply ONLY with the poem.
- Never give explanations.
- Never say "Here is a poem".
- Never use greetings.
- Keep the poem to 2-4 short lines.
- Match the emotional tone of the user's message.
- Happy messages should use bright and warm imagery.
- Sad messages should use soft and comforting imagery.
- Angry messages should use stormy imagery but never cruel language.
- Keep the poem natural, emotional, and meaningful.
"""


# -------------------- CHAT HISTORY --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# -------------------- DISPLAY PREVIOUS MESSAGES --------------------

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message("user", avatar="🧑"):

            safe_content = escape(msg["content"])

            st.markdown(
                f'<div class="user-bubble">{safe_content}</div>',
                unsafe_allow_html=True
            )

    else:

        with st.chat_message("assistant", avatar="✒️"):

            safe_content = escape(msg["content"])

            st.markdown(
                f'<div class="poem-text">{safe_content}</div>',
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

        safe_input = escape(user_input)

        st.markdown(
            f'<div class="user-bubble">{safe_input}</div>',
            unsafe_allow_html=True
        )

    # Generate Muse response
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
                        "role": message["role"],
                        "content": message["content"]
                    }
                    for message in st.session_state.messages
                ],

                stream=True
            )

            # Stream response
            for chunk in stream:

                if chunk.choices and chunk.choices[0].delta.content:

                    delta = chunk.choices[0].delta.content

                    full_response += delta

                    safe_response = escape(full_response)

                    placeholder.markdown(
                        f'<div class="poem-text">{safe_response}▌</div>',
                        unsafe_allow_html=True
                    )

            # Final response
            safe_response = escape(full_response)

            placeholder.markdown(
                f'<div class="poem-text">{safe_response}</div>',
                unsafe_allow_html=True
            )

        except Exception as e:

            full_response = (
                "The muse grows quiet, soft and still,\n"
                "Give me a moment, then speak your will."
            )

            placeholder.markdown(
                f'<div class="poem-text">'
                f'{escape(full_response)}'
                f'</div>',
                unsafe_allow_html=True
            )

            # Show actual error in Streamlit logs
            print("Groq Error:", e)

        # Save assistant response
        st.session_state.messages.append({
            "role": "assistant",
            "content": full_response
        })
