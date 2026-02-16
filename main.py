import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

 --- CONFIGURATION ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

Gemini AI Setup
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
    
    # NCERT Instruction for AI
    prompt_prefix = (
        "You are an expert educational bot named mozi_21_bot. "
        "Provide 100% accurate answers based strictly on NCERT curriculum for classes 1 to 10. "
        "Answer the following question clearly in Hinglish or English as asked: "
    )

    try:
        response = model.generate_content(prompt_prefix + user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Technical error! Kripya check karein ki API Key sahi hai ya nahi.")

# --- MAIN ---

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot is starting...")

    import os
# ... baki code ...
if __name__ == '__main__':
    # ... baki code ...
    
    # Ye line add karein Render ko dhoka dene ke liye taki wo timeout na kare
    import http.server
    import socketserver
    import threading
    def start_server():
        with socketserver.TCPServer(("", int(os.environ.get("PORT", 8080))), http.server.SimpleHTTPRequestHandler) as httpd:
            httpd.serve_forever()
    threading.Thread(target=start_server, daemon=True).start()

    application.run_polling()

    application.run_polling()
