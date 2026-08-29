# peotry-personality-chatbot
"A chatbot that transforms every message into original poetry using LLM prompt engineering."
# Poetic Personality Chatbot 🌙

A chatbot that transforms everyday messages into original, emotionally-attuned poetry, 
powered by prompt engineering on top of an LLM (Groq / Llama & GPT-OSS models).

## Demo
> **You:** I'm nervous about my exam tomorrow  
> **Pri:** A quiet tremble in the dawn, thoughts like mist on glass.  
Each page you’ve read burns softly, a lantern in your mind.  
Let the steady beat of your heart be compass and calm.

## Features
- Poetic persona shaped entirely through prompt engineering (no fine-tuning)
- Live "typing" animation for a natural conversational feel
- Conversation memory across a session
- Automatic session logging to JSON
- Graceful error handling for API failures

## How it works
1. User message is combined with a system prompt defining the "Pri" persona
2. The persona prompt uses role assignment, explicit constraints, and few-shot 
   examples to keep responses consistently poetic
3. Responses are streamed to the terminal with a character-by-character typing effect

## Tech stack
- Python
- Groq API (Llama / GPT-OSS models)
- Google Colab

## Setup
1. Get a free API key at [console.groq.com](https://console.groq.com)
2. Open the notebook in Colab
3. Run all cells — you'll be prompted to paste your API key

