from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler, ContextTypes

from config import TELEGRAM_TOKEN
from transcript import get_transcript
from summarizer import summarize, answer_question, translate_text


user_sessions = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send a YouTube link 🎥")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        lower_text = text.lower()
        user_id = update.message.from_user.id

        # ---------------------------
        # 1️⃣ Handle YouTube Link
        # ---------------------------
        if "youtube.com" in lower_text or "youtu.be" in lower_text:

            await update.message.reply_text("Fetching transcript...")

            transcript, error = get_transcript(text)

            if error:
                await update.message.reply_text(error)
                return

            user_sessions[user_id] = {
                "transcript": transcript,
                "summary": None
            }

            await update.message.reply_text("Generating summary...")

            summary = summarize(transcript)

            if not summary:
                summary = "Model returned empty summary."

            user_sessions[user_id]["summary"] = summary

            await update.message.reply_text(summary)
            return


        # ---------------------------
        # 2️⃣ Hindi Summary Request
        # ---------------------------
        if "summarize in hindi" in lower_text:

            if user_id not in user_sessions:
                await update.message.reply_text("Please send a YouTube link first.")
                return

            await update.message.reply_text("Translating to Hindi...")

            english_summary = user_sessions[user_id]["summary"]

            if not english_summary:
                await update.message.reply_text("No summary available.")
                return

            hindi_summary = translate_text(english_summary, "Hindi")

            if not hindi_summary:
                hindi_summary = "Translation failed."

            await update.message.reply_text(hindi_summary)
            return


        # ---------------------------
        # 3️⃣ Q&A Handling
        # ---------------------------
        if user_id not in user_sessions:
            await update.message.reply_text("Please send a YouTube link first.")
            return

        transcript = user_sessions[user_id]["transcript"]

        # Detect Hindi characters
        is_hindi = any('\u0900' <= c <= '\u097F' for c in text)

        if is_hindi:
            # Step 1: Translate Hindi → English
            translated_question = translate_text(text, "English")

            # Step 2: Get grounded English answer
            english_answer = answer_question(transcript, translated_question)

            if not english_answer:
                english_answer = "Model returned empty response."

            if english_answer.strip() == "This topic is not covered in the video.":
                await update.message.reply_text("यह विषय इस वीडियो में शामिल नहीं है।")
            else:
        # Return stable English answer
                await update.message.reply_text(english_answer)

        else:
            # English flow
            answer = answer_question(transcript, text)

            if not answer:
                answer = "Model returned empty response."

            await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"Unexpected error: {str(e)}")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()


if __name__ == "__main__":
    main()