from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будем писать наш код :)

async def start(update, context):
    await send_photo(update, context, "main")
    text = load_message("main")
    await send_text(update, context, "*Ты нажал на start\n*" + text)

async def hello(update, context):
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

app = ApplicationBuilder().token("7442085622:AAEMZEDduTPxq00E-3HD1YXB1Y98dZw-EW0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
