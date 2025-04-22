
# 💬 FeelGoodBot 😄  
A kind and empathetic AI chatbot for emotional wellness, built using **Streamlit** and **OpenRouter (Mixtral)**.  
Supports affirmations, emotion detection, journaling mode, and memory logging — all in one beautiful package.  

---

## 🌟 Features

- 🤗 Emotion-aware responses
- 🧠 Memory-based conversation tracking
- 🌈 One-tap positive affirmations
- 📝 Journaling mode with prompt-based reflections
- ⏳ Smooth UX with "bot is typing…" spinner
- ⚡️ Lightweight, local, and private
- 💻 Mac-compatible setup (tested)

---

## 🚀 Getting Started

### 🔧 How to Run (macOS/Linux)

1. **Clone the repo or unzip the project folder**
   ```bash
   cd your-project-folder
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

4. **Upgrade pip (optional but recommended)**
   ```bash
   python3 -m pip install --upgrade pip
   ```

5. **Install dependencies**
   ```bash
   python3 -m pip install --no-user -r requirements.txt
   ```

6. **Create a `.env` file with your API key**
   ```bash
   echo 'OPENROUTER_API_KEY=your_openrouter_key_here' > .env
   ```

7. **Run the app**
   ```bash
   streamlit run feelgoodbot.py
   ```

---

## 📂 Folder Structure

```
FeelGoodBot/
├── feelgoodbot.py          # Main Streamlit app
├── .env                    # Your API key (excluded via .gitignore)
├── .gitignore              # Prevents .env and cache files from uploading
├── memory.json             # Chat + mood logs
├── journal.json            # Journal entries
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🧠 Version Timeline

| Version | Status            | Description                            |
|---------|-------------------|----------------------------------------|
| `v1.1`  | ✅ Stable          | Core functionality with emotion tracking + memory |
| `v1.2`  | ✅ Stable          | Added typing spinner UX                |
| `v1.4`  | ✅ Stable          | Introduced journal memory and prompt history |
| `v1.5`  | ✅ Stable          | Refined UI and styling                 |
| `v1.6`  | ✅ Stable          | Journaling mode with reflection prompts |

> You can roll back to any version by checking out earlier commits or branches.

---

## 🔐 API Key Info

This app uses **OpenRouter** to generate responses.

🛡️ Keep your API key secure:
- Your `.env` file is ignored by Git
- Never hardcode the key in your script

---

## ❤️ Credits

Built by [Shivam](https://github.com/shivam)  
Powered by:
- [Streamlit](https://streamlit.io/)
- [OpenRouter (Mixtral)](https://openrouter.ai)

---

## 📸 Preview

> Coming soon: hosted version or screenshot preview link.

---

## ⭐️ Like it? Star it!

If this project made you smile even once — give it a ⭐️ on GitHub!
