import re
import os
from flask import Flask
from threading import Thread
from simpleeval import simple_eval
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- Website Setup ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port, debug=False)

# --- Bot Token ---
TOKEN = "8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM"

def mm_to_en_numbers(text):
    mm_nums = '၀၁၂၃၄၅၆၇၈၉'
    en_nums = '0123456789'
    table = str.maketrans(mm_nums, en_nums)
    return text.translate(table)

def clean_and_calculate(expression):
    expression = mm_to_en_numbers(expression)
    # ဒီမှာ '/' ကို '÷' အဖြစ်မပြောင်းတော့ဘဲ ÷ ကိုပဲ / ပြောင်းပြီးတွက်ပါမယ်
    cleaned = expression.replace('×', '*').replace('÷', '/')
    try:
        if not any(op in cleaned for op in "+-*/"):
            return None
        return simple_eval(cleaned)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    
    user_text = update.message.text

    # --- 🟢 ပြင်ဆင်လိုက်တဲ့အပိုင်း ---
    # ၁။ စာသားထဲမှာ '/' ပါရင် လုံးဝ အလုပ်မလုပ်ခိုင်းတော့ပါဘူး
    if '/' in user_text:
        return

    # ၂။ စာလုံး (A-Z) သို့မဟုတ် မြန်မာစာပါရင်လည်း ကျော်သွားမယ်
    if re.search(r'[a-zA-Z\u1000-\u1021]', user_text):
        return

    # ဂဏန်းနဲ့ သင်္ချာသင်္ကေတ သီးသန့်ပဲပါတဲ့ စာကိုရှာမယ် (ဒီထဲမှာ '/' ကို ဖယ်ထားပါတယ်)
    math_patterns = re.findall(r'[0-9၀-၉+\-*×÷.\s]{3,}', user_text)
    calc_results = []
    
    for item in math_patterns:
        item = item.strip()
        res = clean_and_calculate(item)
        if res is not None:
            if isinstance(res, float): 
                res = round(res, 2)
            calc_results.append(f"{item} = {res}")

    if calc_results:
        result_str = "\n".join(calc_results)
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
    Thread(target=run_web).start()
    
    print("Bro Style Calculator Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
