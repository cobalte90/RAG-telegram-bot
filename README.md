# 🤖 RAG-Powered Telegram Bot
## Welcome! This is my Retrieval-Augmented Generation (RAG) system implemented as a Telegram bot.

## ✨ Key Features
Store notes in any format:   
📝 Text messages   
🎙️ Voice recordings

## Ask questions (via text or voice) and get context-aware answers based on your saved notes.

## 🛠 How It Works
Send your notes (text or voice).

Query the bot naturally — it retrieves and synthesizes answers from your data.   

# Structure
```
notes_bot/   
├── 📁 db/                   # Database files (auto-generated)   
│   
├── 📄 chroma_db.py          # 🧠 Vector DB setup (Chroma)   
├── 📄 database.py           # 💾 SQL DB for note storage     
├── 📄 llm_processing.py     # ✨ Mistral AI text processing   
├── 📄 notes_bot_main.py     # 🤖 Core bot logic   
│   
├── 📄 .env.                 # ⚙️ Environment   
└── 📄 requirements.txt      # 📦 Dependencies   
```
