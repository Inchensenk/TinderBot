from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

async def start(update, context):
    dialog.mode = "main"
    await send_photo(update, context, "main")
    text = load_message("main")
    await send_text(update, context, "*Ты нажал на start\n*" + text)

    await show_main_menu(update, context, {
        "start":"Главное меню бота",
        "profile":"генерация Tinder-профля 😎",
        "opener": "сообщение для знакомства 🥰",
        "message": "переписка от вашего имени 😈",
        "date": "переписка со звездами 🔥",
        "gpt": "задать вопрос чату GPT 🧠"
    })

async def gpt(update, context):
    dialog.mode = "gpt"
    text = load_message("gpt")
    await send_photo(update, context, "gpt")
    await send_text(update, context, text)

async def gpt_dialog(update, context):
    text = update.message.text
    prompt = load_prompt("gpt")
    answer = await chatgpt.send_question(prompt,text)
    await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    else:
        await send_text(update, context,"*Привед Медвед*")
        await send_text(update, context, "_Как твоё ничего?_")
        await send_text(update, context, "Вы написали: " + update.message.text)

        await send_photo(update, context, "avatar_main")
        await send_text_buttons(update, context, "Запустить ракету?", {
            "start":"Запустить ракету",
            "stop":"Остановить ракету"
        })

async def hello_button(update, context):
    query = update.callback_query.data
    if query == "start":
        await send_text(update, context,"*Ракета полетела*")
    else:
        await send_text(update, context,"*Ракета остановлена, летит обратно*")

dialog = Dialog()
dialog.mode = None

chatgpt = ChatGptService(token="gpt:EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd")

app = ApplicationBuilder().token("7442085622:AAEMZEDduTPxq00E-3HD1YXB1Y98dZw-EW0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
