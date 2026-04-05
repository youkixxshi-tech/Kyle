import re
from simpleeval import simple_eval
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# မင်းရဲ့ Bot Token ကို ဒီမှာ ထည့်ပါ
TOKEN = "8428492734:AAGI_E83LLQBHaDvpRJw0wWAMCj0aDlrWKM"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text: return

    # ၁။ ဂဏန်းတွေကိုပဲ သီးသန့် ဆွဲထုတ်ခြင်း (Copy Bot လုပ်ဆောင်ချက်)
    # စာသားထဲက ဂဏန်းအားလုံးကို ရှာမယ်
    all_numbers = re.findall(r'\d+', text)
    parsed_result = " ".join(all_numbers)

    # ၂။ သင်္ချာပုစ္ဆာ ရှာဖွေတွက်ချက်ခြင်း (Calculator လုပ်ဆောင်ချက်)
    math_problems = re.findall(r'[0-9+\-*/().\s]{3,}', text)
    calc_results = []
    
    for p in math_problems:
        p = p.strip()
        if any(c in p for c in "+-*/"):
            try:
                res = simple_eval(p)
                calc_results.append(f"{p} = {res}")
            except:
                continue

    # အဖြေပြန်ပို့မည့် အပိုင်း
    response = ""
    
    # Copy ကူးဖို့ ဂဏန်းတွေရှိရင် ထည့်မယ်
    if parsed_result:
        # Markdown မှာ ` ` (backticks) နဲ့ အုပ်ထားရင် ဖုန်းမှာ နှိပ်လိုက်တာနဲ့ Copy ဖြစ်ပါတယ်
        response += f"📋 **Parsed Data (Click to Copy):**\n`{parsed_result}`\n\n"

    # တွက်ချက်မှုရလဒ်ရှိရင် ထည့်မယ်
    if calc_results:
        response += "📊 **Calculation:**\n" + "\n".join(calc_results)

    if response:
        await update.message.reply_text(response, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot is starting...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
