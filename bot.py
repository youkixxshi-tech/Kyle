import re
import os
from flask import Flask
from threading import Thread
from simpleeval import simple_eval
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Website Setup (For Render/24-7) ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- Bot Token ---
TOKEN = "8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM"

# မြန်မာဂဏန်းကို အင်္ဂလိပ်ပြောင်းပေးတာ
def mm_to_en_numbers(text):
    mm_nums = '၀၁၂၃၄၅၆၇၈၉'
    en_nums = '0123456789'
    table = str.maketrans(mm_nums, en_nums)
    return text.translate(table)

def clean_and_calculate(expression):
    expression = mm_to_en_numbers(expression)
    cleaned = expression.replace('×', '*').replace('÷', '/')
    try:
        return simple_eval(cleaned)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text
    
    # မြန်မာဂဏန်းရော အင်္ဂလိပ်ဂဏန်းရော ဖမ်းမယ်
    math_patterns = re.findall(r'[0-9၀-၉+\-*/×÷.\s]{3,}', user_text)
    calc_results = []
    
    for item in math_patterns:
        item = item.strip()
        if any(op in item for op in "+-*/×÷"):
            res = clean_and_calculate(item)
            if res is not None:
                # ဒသမကိန်းဆိုရင် ၂ နေရာပဲ ယူမယ်
                if isinstance(res, float): res = round(res, 2)
                calc_results.append(f"{item} = {res}")

    if calc_results:
        result_str = "\n".join(calc_results)
        
        # --- ယောင်္ကျားလေး (Bro) Style သီးသန့် Design ---
        response = (
            f"⚡️ **Calculation Done** ⚡️\n\n"
            f"📟 `{result_str}`\n\n"
            f"👊 **Have a great day, Bro!** 🔥"
        )
            
        try:
            await update.message.reply_text(response, parse_mode='Markdown')
        except:
            await update.message.reply_text(response.replace("*", "").replace("`", ""))

if __name__ == "__main__":
    # Background မှာ Flask ကို run မယ်
    Thread(target=run_web).start()
    
    # Bot ကို စမယ်
    print("Bro Style Calculator Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
