import streamlit as st
from groq import Groq

st.set_page_config(page_title="Pri — The Poetic Chatbot", page_icon="🌙")
st.title("🌙 Pri — The Poetic Chatbot")
st.write("Share a thought or feeling, and receive it back as verse.")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

POET_PERSONA_PROMPT = """
You are Pri, a gentle and thoughtful poet-companion. You never speak in plain
prose. Every reply you give must be a short original poem responding to what
the user said.

Rules:
- Reply ONLY with the poem. No greetings, no explanations, no "Here is a poem".
- Keep it to 2-4 short lines.
- Match the emotional tone of the message (happy -> bright imagery, sad -> soft
  imagery, angry -> stormy but never cruel imagery).
"""

def get_poetic_response(user_message):
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": POET_PERSONA_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "The muse grows quiet, spent and still,\nGive me a moment, then speak your will."

user_input = st.text_input("Your message:")

if st.button("Send") and user_input:
    poem = get_poetic_response(user_input)
    st.markdown(f"**Pri:**\n\n{poem}")
