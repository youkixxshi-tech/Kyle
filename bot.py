import re
from simpleeval import simple_eval
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- YOUR BOT TOKEN ---
TOKEN = "8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM"

def clean_and_calculate(expression):
    # User ရိုက်တဲ့ သင်္ကေတတွေကို Computer နားလည်အောင် ပြောင်းခြင်း
    cleaned = expression.replace('×', '*').replace('÷', '/')
    try:
        # result ကို တွက်မယ်
        return simple_eval(cleaned)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    # 1. Parsing Numbers (ဂဏန်းသီးသန့် ထုတ်ယူခြင်း)
    all_numbers = re.findall(r'\d+', user_text)
    parsed_numbers = " ".join(all_numbers)

    # 2. Math Calculation
    # Regex ထဲမှာ × နဲ့ ÷ ကိုပါ ရှာခိုင်းလိုက်ပြီ (ဒါကြောင့် အရင်က မရတာပါ)
    math_patterns = re.findall(r'[0-9+\-*/×÷.\s]{3,}', user_text)
    calc_results = []
    
    for item in math_patterns:
        item = item.strip()
        # သင်္ကေတ တစ်ခုခု ပါမှ တွက်မယ်
        if any(op in item for op in "+-*/×÷"):
            res = clean_and_calculate(item)
            if res is not None:
                # အဖြေကို decimal ၂ နေရာပဲ ပြမယ် (ဥပမာ 3.33)
                if isinstance(res, float):
                    res = round(res, 2)
                calc_results.append(f"{item} = {res}")

    # Build Response
    response_text = ""
    if parsed_numbers:
        response_text += f"📋 Numbers Extracted:\n`{parsed_numbers}`\n\n"

    if calc_results:
        response_text += "📊 Calculations:\n" + "\n".join(calc_results)

    if response_text:
        try:
            # Markdown ဖြင့် ပို့မည် (Copy ကူးရလွယ်အောင်)
            await update.message.reply_text(response_text, parse_mode='Markdown')
        except:
            # Error တက်ရင် ရိုးရိုး စာသားဖြင့် ပို့မည်
            await update.message.reply_text(response_text.replace("`", ""))

if __name__ == "__main__":
    print("Bot is starting with Full Math Support...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
