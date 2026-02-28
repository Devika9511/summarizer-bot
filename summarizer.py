import requests
from config import OLLAMA_MODEL


def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "options": {
                    "temperature": 0.1,
                    "num_predict": 200
                },
                "stream": False
            },
            timeout=60
        )

        data = response.json()

        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()

        return "Model returned empty response."

    except Exception as e:
        return f"Model error: {str(e)}"


# -----------------------
# Structured Summary
# -----------------------
def summarize(transcript):

    trimmed = transcript[:1200]

    prompt = f"""
You are a strict AI research assistant.

Follow the format EXACTLY.
Do NOT add extra sections.
Do NOT write paragraph summary.

Return exactly:

🎥 Video Title:
<Short clear title>

📌 5 Key Points:
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

⏱ Important Timestamps:
If not mentioned, write:
Not explicitly mentioned in transcript.

🧠 Core Takeaway:
Maximum 4 concise lines.

Transcript:
{trimmed}
"""

    return call_ollama(prompt)


# -----------------------
# Grounded Q&A
# -----------------------
def answer_question(transcript, question):

    trimmed = transcript[:1200]

    prompt = f"""
You are a strict transcript-based assistant.

You MUST follow these rules:

1. Use ONLY information explicitly stated in the transcript.
2. Do NOT use general knowledge.
3. Do NOT define concepts unless clearly defined in transcript.
4. If the transcript does NOT clearly explain the answer, reply EXACTLY:
This topic is not covered in the video.

Keep answer short (maximum 4 lines).
No code examples.
No extra explanation.

Transcript:
{trimmed}

Question:
{question}
"""

    return call_ollama(prompt)


# -----------------------
# Translation Layer
# -----------------------
def translate_text(text, language):

    prompt = f"""
Translate the following text into {language}.
Translate only.
Do NOT add explanations.
Preserve bullet points.

Text:
{text}
"""

    return call_ollama(prompt)