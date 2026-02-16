import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# --- CONFIGURATION ---
TELEGRAM_TOKEN = "8318157415:AAECQ2wWSwAY8aWzsqw96hccEbH-3ds4KU8"
GEMINI_API_KEY = "AIzaSyAPwgotRtvnGIYTWdekthF2S5HoyVTrXY8"

# Gemini AI Setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- FUNCTIONS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Keyboard Buttons
    keyboard = [
        ["1) Aap mujse kya Janna chate hain? 🥰"],
        ["2) Aur Knowledge?", "3) Koi questions ka answer?"],
        ["4) English Grammar?", "5) Class 10 ka question answer?"],
        ["6) Class 9 ka question answer?", "7) Class 8 ka question answer?"],
        ["8) Class 7 ka question answer?", "9) Class 6 ka question answer?"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    welcome_msg = (
        f"Namaste! Main hoon **@mozi_21_bot**.\n\n"
        "Main Class 1 se 10 tak NCERT ke sabhi subjects aur English Grammar mein aapki madad kar sakta hoon.\n"
        "Mujhse kuch bhi puchiye, main 100% sahi jawab dene ki koshish karunga!"
    )
    await update.message.reply_text(welcome_msg, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.message.chat_id

    # Bot ko instruction dena ki wo NCERT expert ki tarah behave kare
    prompt_prefix = (
        "You are an expert educational bot named mozi_21_bot. "
        "Provide 100% accurate answers based strictly on NCERT curriculum for classes 1 to 10. "
        "Answer the following question clearly and correctly: "
    )

    try:
        # AI se answer mangna
        response = model.generate_content(prompt_prefix + user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Maafi chahta hoon, abhi thodi dikkat ho rahi hai. Kripya thodi der baad koshish karein.")

# --- MAIN ---

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is running...")
    application.run_polling()
