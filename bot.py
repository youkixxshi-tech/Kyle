import re
import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM")

def extract_and_calculate(text):
    problems = re.findall(r'[0-9+\-*/().\s]+', text)
    results = []
    
    for p in problems:
        p = p.strip()
        if len(p) >= 3 and any(c in p for c in "+-*/"):
            try:
                res = eval(p)
                results.append(f"{p} = {res}")
            except:
                continue
    return "\n".join(results)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    answer = extract_and_calculate(user_text)
    
    if answer:
        await update.message.reply_text(f"Calculation Result:\n{answer}")

if __name__ == "__main__":
    print("Bot is running...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
