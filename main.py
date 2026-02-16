import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
 #--- CONFIGURATION ---
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
 #Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# --- RENDER TIMEOUT FIX (FAKE SERVER) ---

# --- FUNCTIONS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["1) Aap mujse kya Janna chate hain? 🥰"],
        ["2) Aur Knowledge?", "3) Koi questions ka answer?"],
        ["4) English Grammar?", "5) Class 10 ka question answer?"],
        ["6) Class 9 ka question answer?", "7) Class 8 ka question answer?"],
        ["8) Class 7 ka question answer?", "9) Class 6 ka question answer?"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    welcome_msg = "Namaste! Main hoon **@mozi_21_bot**. Main NCERT expert hoon. Kuch bhi puchiye!"
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    prompt_prefix = "You are an expert NCERT teacher for classes 1-10. Answer this accurately: "
    try:
        response = model.generate_content(prompt_prefix + user_text)
        await update.message.reply_text(response.text)
    except Exception:
        await update.message.reply_text("Technical error! API Key check karein.")

# --- MAIN ---
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is starting...")

    application.run_webhook(
        listen="0.0.0.0",
        port=port,
        webhook_url="https://mozi-21-bot.onrender.com/" + TELEGRAM_TOKEN)
