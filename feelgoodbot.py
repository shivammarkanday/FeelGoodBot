import streamlit as st
import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import random

# --- Load API Key ---
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

# --- Streamlit Config ---
st.set_page_config(page_title="FeelGoodBot", page_icon="🧠", layout="centered")
st.title("💬 FeelGoodBot")
st.caption("Your kind AI buddy for good vibes ✨")

# --- File Paths ---
MEMORY_FILE = "memory.json"
JOURNAL_FILE = "journal.json"

# --- Journal Prompts ---
prompts = [
    "📝 What made you smile today?",
    "📝 What are you proud of this week?",
    "📝 Something you're grateful for right now?",
    "📝 What’s been on your mind lately?",
    "📝 Describe a recent small win.",
]

# --- Session State Init ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "system", "content": "You are a kind and empathetic AI wellness assistant. Always support the user with warmth and emotional care."}
    ]
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False
if "waiting_for_reply" not in st.session_state:
    st.session_state.waiting_for_reply = False
if "journal_mode" not in st.session_state:
    st.session_state.journal_mode = False
if "journal_prompt" not in st.session_state:
    st.session_state.journal_prompt = ""
if "journal_entries" not in st.session_state:
    st.session_state.journal_entries = []

# --- Emotion Detection ---
def detect_emotion(text):
    text = text.lower()
    sad = ["sad", "tired", "angry", "anxious", "upset", "lonely"]
    happy = ["happy", "excited", "joy", "grateful", "peaceful"]
    neutral = ["okay", "fine", "meh", "neutral", "thinking"]
    for word in sad:
        if word in text:
            return "sad"
    for word in happy:
        if word in text:
            return "happy"
    for word in neutral:
        if word in text:
            return "neutral"
    return "neutral"

# --- Save normal message to memory.json ---
def save_message(user_msg, bot_msg, mood):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user": user_msg,
        "bot": bot_msg,
        "mood": mood
    }
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Save journal prompt + response (session + file) ---
def save_journal_entry(prompt, response):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    st.session_state.journal_entries.append(entry)

    try:
        with open(JOURNAL_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append(entry)
    with open(JOURNAL_FILE, "w") as f:
        json.dump(data, f, indent=2)

# --- Get AI response from OpenRouter ---
def get_bot_reply(chat_history):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": chat_history
        }
    )
    if response.status_code != 200:
        st.error(f"API Error {response.status_code}")
        return None
    return response.json()["choices"][0]["message"]["content"]

# --- Show chat history ---
st.markdown("### 💬 Conversation")
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**FeelGoodBot:** {msg['content']}")

# --- Show current journal prompt ---
if st.session_state.journal_mode and st.session_state.journal_prompt:
    st.markdown(f"#### ✍️ Journal Prompt: *{st.session_state.journal_prompt}*")

# --- Affirmation Button ---
if st.button("🌈 Give me a kind affirmation", disabled=st.session_state.waiting_for_reply or st.session_state.journal_mode):
    st.session_state.chat_history.append({"role": "user", "content": "[Affirmation Request]"})
    st.session_state.waiting_for_reply = True
    with st.spinner("💬 FeelGoodBot is typing..."):
        reply = get_bot_reply(st.session_state.chat_history)
    if reply:
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        save_message("[Affirmation Request]", reply, "neutral")
    st.session_state.clear_input = True
    st.session_state.waiting_for_reply = False
    st.rerun()

# --- Input Form ---
st.markdown("---")
with st.form("chat_form", clear_on_submit=False):
    col1, col2, col3 = st.columns([7, 1, 1])
    with col1:
        user_input = st.text_input(
            "Type your message...",
            key="user_input",
            value="" if st.session_state.clear_input else st.session_state.get("user_input", ""),
            label_visibility="collapsed",
            disabled=st.session_state.waiting_for_reply
        )
    with col2:
        submitted = st.form_submit_button("📤", disabled=st.session_state.waiting_for_reply)
    with col3:
        toggle_journal = st.form_submit_button("📝", disabled=st.session_state.waiting_for_reply)

# --- Journal Toggle ---
if toggle_journal:
    if not st.session_state.journal_mode:
        st.session_state.journal_mode = True
        st.session_state.journal_prompt = random.choice(prompts)
    else:
        st.session_state.journal_mode = False
        st.session_state.journal_prompt = ""
        st.session_state.chat_history.append({"role": "assistant", "content": "*{journal mode ended}*"})
    st.rerun()

# --- Handle Submission ---
if submitted:
    user_input = user_input.strip()
    if user_input and api_key:
        if st.session_state.journal_mode:
            prompt = st.session_state.journal_prompt
            st.session_state.chat_history.append({"role": "assistant", "content": f"✍️ {prompt}"})
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            save_journal_entry(prompt, user_input)
            st.session_state.journal_prompt = random.choice(prompts)
        else:
            st.session_state.waiting_for_reply = True
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            mood = detect_emotion(user_input)
            with st.spinner("💬 FeelGoodBot is typing..."):
                reply = get_bot_reply(st.session_state.chat_history)
            if reply:
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                save_message(user_input, reply, mood)
            st.session_state.waiting_for_reply = False
        st.session_state.clear_input = True
        st.rerun()

# --- Memory Viewer ---
with st.expander("🧠 View My Memory"):
    try:
        with open(MEMORY_FILE, "r") as f:
            memory_data = json.load(f)
        for entry in reversed(memory_data[-10:]):
            st.markdown(f"🕒 `{entry['timestamp']}`")
            st.markdown(f"**You:** {entry['user']}`")
            st.markdown(f"**FeelGoodBot:** {entry['bot']}")
            st.markdown(f"*Mood detected:* `{entry['mood']}`")
            st.markdown("---")
    except:
        st.info("No memory yet. Start chatting!")

# --- Export Journal Button ---
if st.session_state.journal_entries:
    st.markdown("### 📓 Download Your Journal Session")
    export_json = json.dumps(st.session_state.journal_entries, indent=2)
    st.download_button(
        label="📥 Export This Journal Session",
        data=export_json,
        file_name="journal_session.json",
        mime="application/json"
    )

# --- Reset input clear flag ---
if st.session_state.clear_input:
    st.session_state.clear_input = False
