import re
from simpleeval import simple_eval
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- INSERT YOUR BOT TOKEN HERE ---
TOKEN = "8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM"

def clean_and_calculate(expression):
    # User ရိုက်တဲ့ × ကို * အဖြစ်၊ ÷ ကို / အဖြစ် ပြောင်းလဲခြင်း
    cleaned = expression.replace('×', '*').replace('÷', '/')
    try:
        # simple_eval သုံးပြီး ဘေးကင်းစွာ တွက်ချက်ခြင်း
        return simple_eval(cleaned)
    except:
        return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text

    # 1. Parsing Numbers (Easy Copy)
    all_numbers = re.findall(r'\d+', user_text)
    parsed_numbers = " ".join(all_numbers)

    # 2. Math Calculation (Supporting × and ÷)
    # Regex မှာ × နဲ့ ÷ ကိုပါ ရှာခိုင်းထားပါတယ်
    math_patterns = re.findall(r'[0-9+\-*/×÷().\s]{3,}', user_text)
    calc_results = []
    
    for item in math_patterns:
        item = item.strip()
        # သင်္ချာသင်္ကေတ တစ်ခုခုပါမှ တွက်မယ်
        if any(op in item for op in "+-*/×÷"):
            res = clean_and_calculate(item)
            if res is not None:
                calc_results.append(f"{item} = {res}")

    # Build Response
    response_text = ""
    if parsed_numbers:
        response_text += f"📋 **Numbers Extracted:**\n`{parsed_numbers}`\n\n"

    if calc_results:
        response_text += "📊 **Calculations:**\n" + "\n".join(calc_results)

    if response_text:
        await update.message.reply_text(response_text, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is starting with × and ÷ support...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
