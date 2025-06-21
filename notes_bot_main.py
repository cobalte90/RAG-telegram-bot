from telegram import Update
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler
import database
import chroma_db
from llm_processing import llm_response
import tempfile
import whisper
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
whisper_model = whisper.load_model("base")

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
database.init_db()

# show the keyboard when the bot starts
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-помощник.\nТы можешь писать мне заметки текстом или отправлять голосовыми сообщениями.\nПотом я смогу отвечать тебе на основе этих заметок🚀",
        reply_markup=note_keyboard
    )

# keyboard with button to create a note
note_keyboard = ReplyKeyboardMarkup(
    [[KeyboardButton("📝 Создать заметку")]],
    resize_keyboard=True,
    is_persistent=True
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    userid = update.message.from_user.id

    if 'awaiting_note' not in context.user_data:
        context.user_data['awaiting_note'] = False

    # Voice message
    if update.message.voice:
        try:
            voice_file = await update.message.voice.get_file()
            
            with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as f:
                temp_path = f.name
            
            await voice_file.download_to_drive(temp_path)
            
            wav_path = temp_path.replace('.ogg', '.wav')
            subprocess.run(['ffmpeg', '-i', temp_path, '-ar', '16000', '-ac', '1', wav_path], 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            result = whisper_model.transcribe(wav_path, language='ru')
            text = result['text']
            await update.message.reply_text(f"🎤 Распознано: {text}")
            
        except Exception as e:
            print(f"Ошибка обработки голосового: {e}")
            await update.message.reply_text("❌ Не удалось обработать голосовое сообщение")
            return
        finally:
            for f in [temp_path, wav_path]:
                try:
                    if os.path.exists(f):
                        os.unlink(f)
                except:
                    pass
    else:
        text = update.message.text

    # Creating a note
    if text == "📝 Создать заметку":
        context.user_data["awaiting_note"] = True
        await update.message.reply_text("Напишите или отправьте в голосовом вашу заметку")
    
    # Accepts the note text
    elif context.user_data["awaiting_note"]:
        context.user_data["awaiting_note"] = False
        chunk_ids = chroma_db.save_vectorized_note(userid, text)
        database.save_note(userid, text, chunk_ids)
        await update.message.reply_text("Заметка успешно записана! Я запомню её и смогу помочь вам в будущем.")
    
    # User query
    else:
        result = llm_response(text, userid)
        await update.message.reply_text(result)


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_message))    
    app.run_polling()

if __name__ == "__main__":
    main()