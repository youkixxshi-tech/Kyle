from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM")

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        result = eval(text)
        await update.message.reply_text(f"Result: {result}")
    except Exception as e:
        await update.message.reply_text("Error ❌")

app = ApplicationBuilder().token(8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), calculate))

print("Bot is running...")
app.run_polling()
