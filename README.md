📌 Telegram YouTube Summarizer & Q&A Bot
Eywa SDE Intern Assignment
🚀 Project Overview

This project is a Telegram-based AI assistant that helps users quickly understand long YouTube videos and interact with their content intelligently.

The bot can:

🔗 Accept a YouTube link

📜 Extract the video transcript

🧾 Generate a structured summary

❓ Answer contextual follow-up questions

🌍 Support multilingual input (English + Hindi)

The system is designed to behave like a lightweight AI research assistant for YouTube content.

🎯 Objective

The goal is to build a Telegram bot that:

🔗 Accepts a YouTube link

📥 Fetches the video transcript

🧠 Generates a structured summary

💬 Allows contextual Q&A

🌐 Supports English and at least one Indian language

🚫 Ensures grounded responses (no hallucinations)

🧠 Core Features Implemented
1️⃣ Structured Summary Generation

When a user sends a YouTube link, the bot generates:

🎥 Video Title

📌 5 Key Points

⏱ Important Timestamps

🧠 Core Takeaway

✔ The summary format is strictly enforced to avoid long paragraph dumps and improve clarity.

2️⃣ Contextual Q&A (Grounded Responses)

Users can ask multiple follow-up questions about the video.

The system ensures:

📄 Answers are generated strictly using transcript content

🚫 No external knowledge is used

⚠ If the information is not present in the transcript, the bot responds:

"This topic is not covered in the video."

This ensures zero hallucination behavior.

3️⃣ Multi-language Support

The bot supports:

🇬🇧 English (default)

🇮🇳 Hindi input

Implementation Approach

If a user asks a question in Hindi:

🔄 Hindi question is translated into English

🧠 Transcript-based reasoning is performed

💬 Stable response is generated

📢 Hindi fallback responses are used when appropriate

This translation-layer architecture enables multilingual support even on low-resource systems.

🏗 Architecture Design
📂 Project Structure
Summariser/
│
├── bot.py           → Telegram bot logic and session handling
├── transcript.py    → Transcript extraction using yt-dlp
├── summarizer.py    → LLM interaction and structured prompts
├── config.py        → Token and model configuration
└── README.md
🔄 System Flow

1️⃣ User sends a YouTube link
2️⃣ Transcript is extracted using yt-dlp
3️⃣ Transcript is trimmed for memory efficiency
4️⃣ Structured summary is generated using Ollama
5️⃣ User asks follow-up questions
6️⃣ Answers are generated using transcript context only

⚙️ Model & Environment
🧠 LLM Runtime

🖥 Ollama (Local execution)

🤖 Model Used

phi3 (2.2GB model)

💻 System Constraints

RAM: 4GB

GPU: Not available

OS: Windows

⚠ Due to RAM limitations:

❌ Large models like Mistral or LLaMA 3 were not used

✂ Transcript length is trimmed for safe inference

🌡 Temperature reduced for deterministic output

These decisions ensure system stability and reliability.

🔎 Transcript Retrieval Strategy

Transcript extraction is handled using:

yt-dlp --write-auto-sub

The system handles:

❌ Invalid YouTube URLs

⚠ Missing transcripts

📂 Empty subtitle files

📜 Long transcripts

⚙ Command execution errors

Temporary subtitle files are removed after processing.

🧠 Context Management

Each Telegram user session is stored independently using:

user_sessions[user_id]

This ensures:

👥 Multiple users can interact simultaneously

💬 Conversations remain contextual

🔒 Sessions do not interfere with each other

🎯 Q&A Grounding Strategy

The model is explicitly instructed to:

📄 Use only transcript information

🚫 Avoid outside knowledge

❌ Refuse unrelated questions

✏ Provide concise answers (3–5 lines)

This ensures reliable and grounded responses.

🌍 Multi-language Design Decision

Instead of forcing multilingual reasoning inside the model, a translation-layer approach was used:

Hindi → English → Grounded reasoning → Response
Advantages:

✔ Better reliability with small models

✔ Reduced hallucination risk

✔ Works well on low-resource systems

✔ Meets assignment flexibility requirements

🛠 Setup Instructions
1️⃣ Install Ollama

Download from:
https://ollama.com

Pull the model:

ollama pull phi3
2️⃣ Install Python Dependencies

Inside the project folder run:

pip install python-telegram-bot requests yt-dlp
3️⃣ Configure Telegram Bot

Create a bot using BotFather on Telegram

Copy the bot token

Add it inside:

config.py
4️⃣ Run the Bot
python bot.py
⚖ Design Trade-offs

🧠 Lightweight model used due to 4GB RAM constraint

✂ Transcript trimmed to reduce memory usage

🌡 Temperature reduced for structured output

🌍 Translation layer used instead of full multilingual generation

⚡ No embedding pipeline used to keep the system lightweight

🎥 Demo Flow

▶ Start the bot

🔗 Send a YouTube link

📄 Receive structured summary

❓ Ask contextual follow-up questions

🇮🇳 Ask a question in Hindi

⚠ Observe fallback when topic is not covered

📌 Conclusion

This system demonstrates:

🤖 Practical AI assistant development

🧠 Structured prompt engineering

📄 Grounded LLM usage

👥 Multi-user session management

💻 Hardware-aware architecture design

The solution is designed to be stable, scalable, and production-conscious even under constrained hardware resources.
