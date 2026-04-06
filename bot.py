import re
import os
from flask import Flask
from threading import Thread
from simpleeval import simple_eval
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Website အဖြစ် ဟန်ဆောင်ရန် Flask ဆောက်ခြင်း ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is Alive!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- Bot Token ---
TOKEN = "8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM"

def clean_and_calculate(expression):
    cleaned = expression.replace('×', '*').replace('÷', '/')
    try:
        return simple_eval(cleaned)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    
    # တွက်ချက်မှု ပုံစံတွေကို ရှာဖွေခြင်း
    math_patterns = re.findall(r'[0-9+\-*/×÷.\s]{3,}', user_text)
    calc_results = []
    
    for item in math_patterns:
        item = item.strip()
        # အပေါင်းအနှုတ် လက္ခဏာ ပါမပါ စစ်ဆေးခြင်း
        if any(op in item for op in "+-*/×÷"):
            res = clean_and_calculate(item)
            if res is not None:
                if isinstance(res, float): res = round(res, 2)
                # စာသားတွေ မပါဘဲ အဖြေတန်းထုတ်ရန် format ပြင်ခြင်း
                calc_results.append(f"{res}")

    if calc_results:
        # အဖြေကိုပဲ တန်းပြီး ပို့ပေးခြင်း
        response_text = "\n".join(calc_results)
        try:
            await update.message.reply_text(response_text)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    # Website ကို Background မှာ Run ခိုင်းခြင်း
    Thread(target=run_web).start()
    
    # Bot ကို Run ခြင်း
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
