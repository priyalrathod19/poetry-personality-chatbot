
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Muse - The Poetic Chatbot",
    page_icon="✒️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- STYLING --------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600&family=Caveat:wght@500&display=swap');

/* Page background */
.stApp {
    background-color: #f4efe4;
    color: #1a1a1a;
}

/* Reduce excessive top whitespace */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 6rem !important;
    max-width: 720px !important;
}

/* Main title */
h1 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

/* Subtitle */
.subtitle {
    font-family: 'Caveat', cursive;
    font-size: 1.3rem;
    color: #6b6558;
    margin-top: -12px;
    margin-bottom: 25px;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: transparent;
    border-radius: 2px;
    padding: 4px 0;
}

/* User message */
.user-bubble {
    background-color: #e8e1d0;
    border-radius: 8px;
    padding: 10px 14px;
    display: inline-block;
    color: #1a1a1a;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.2rem;
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
}

/* Input */
.stChatInput textarea {
    font-family: 'Cormorant Garamond', serif !important;
    font-style: italic;
    background-color: #fffdf8;
}

/* Hide Streamlit's top header space */
header[data-testid="stHeader"] {
    background-color: transparent;
}

/* Mobile spacing */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

/* Sticky Muse header */
.muse-header {
    position: sticky;
    top: 0;
    z-index: 9999;

    background-color: #f4efe4;

    padding: 15px 0 18px 0;
    margin-top: -10px;
    margin-bottom: 20px;

    border-bottom: 1px solid #ded6c6;
}

/* Muse title */
.muse-brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

/* Pen icon */
.muse-icon {
    font-size: 2.5rem;
}

/* Muse text */
.muse-name {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.8rem;
    font-weight: 600;
    color: #1a1a1a;
    line-height: 1.1;
}

/* Tagline */
.muse-tagline {
    font-family: 'Caveat', cursive;
    font-size: 1.3rem;
    color: #6b6558;
    margin-top: 5px;
    margin-left: 4px;
}

</style>
""", unsafe_allow_html=True)


# -------------------- MUSE HEADER --------------------

st.markdown("""
<div class="muse-header">
    <div class="muse-brand">
        <span class="muse-icon">✒️</span>
        <span class="muse-name">Muse</span>
    </div>
    <div class="muse-tagline">
        turn thoughts into poetry
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------- GROQ CLIENT --------------------

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

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


# Display messages directly on the page.
# No fixed-height chat container.

for msg in st.session_state.messages:

    if msg["role"] == "user":

        with st.chat_message("user", avatar="🧑"):
            st.markdown(
                f'<div class="user-bubble">'
                f'{msg["content"]}</div>',
                unsafe_allow_html=True
            )

    else:

        with st.chat_message("assistant", avatar="✒️"):
            st.markdown(
                f'<div class="poem-text">'
                f'{msg["content"]}</div>',
                unsafe_allow_html=True
            )


# -------------------- CHAT INPUT --------------------

user_input = st.chat_input(
    "Tell Muse what's on your mind..."
)


# -------------------- GENERATE RESPONSE --------------------

if user_input:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Display user message immediately
    with st.chat_message("user", avatar="🧑"):
        st.markdown(
            f'<div class="user-bubble">'
            f'{user_input}</div>',
            unsafe_allow_html=True
        )

    # Generate Muse's response
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

            for chunk in stream:

                delta = chunk.choices[0].delta.content or ""
                full_response += delta

                placeholder.markdown(
                    f'<div class="poem-text">'
                    f'{full_response}▌</div>',
                    unsafe_allow_html=True
                )

            # Final response without cursor
            placeholder.markdown(
                f'<div class="poem-text">'
                f'{full_response}</div>',
                unsafe_allow_html=True
            )

        except Exception:

            full_response = (
                "The muse grows quiet, spent and still,\n"
                "Give me a moment, then speak your will."
            )

            placeholder.markdown(
                f'<div class="poem-text">'
                f'{full_response}</div>',
                unsafe_allow_html=True
            )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": full_response
    })
