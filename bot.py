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


async def date(update, context):
    dialog.mode = "date"
    text = load_message("date")
    await send_photo(update, context, "date")
    await send_text_buttons(update, context, text, {
        "dateGrande":"Ариана Гранде",
        "dateRobbie": "Марго Робби",
        "dateZendaya": "Зендея",
        "dateGosling": "Райан Гослинг",
        "dateHardy": "Том Харди"
    })

async def date_dialog(update, context):
    text = update.message.text
    my_message = await send_text(update, context, "Девушка набирает текст...")
    answer = await chatgpt.add_message(text)
    await my_message.edit_text(answer)

async def date_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    await send_photo(update, context, query)
    await send_text(update, context, "Отличный выбор! Пригласите девушку или парня на свидание за 5 сообщений ")

    prompt = load_prompt(query)
    chatgpt.set_prompt(prompt)


async def message(update, context):
    dialog.mode = "message"
    text = load_message("message")

    await send_photo(update, context, "message")
    await send_text_buttons(update, context, text, {
        "messageNext":"Следующее сообщение",
        "messageDate":"Пригласить на свидание"
    })
    dialog.list.clear()

async def message_button(update, context):
    query = update.callback_query.data
    await update.callback_query.answer()

    prompt = load_prompt(query)
    user_chat_history = "\n\n".join(dialog.list)
    my_message = await send_text(update, context, "ChatGPT думает над вариантами ответа...")
    answer = await chatgpt.send_question(prompt, user_chat_history)
    await my_message.edit_text(answer)

async def message_dialog(update, context):
    text = update.message.text
    dialog.list.append(text)

async def profile(update, context):
    dialog.mode = "profile"
    text = load_message("profile")
    await send_photo(update, context, "profile")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.counter = 0
    await send_text(update, context, "Сколько тебе лет?")

async def profile_dialog(update, context):
    text = update.message.text
    dialog.counter += 1

    if dialog.counter == 1:
        dialog.user["age"] = text
        await send_text(update, context, "Кем ты работаешь?")
    elif dialog.counter == 2:
        dialog.user["occupation"] = text
        await send_text(update, context, "У тебя есть хобби?")
    elif dialog.counter == 3:
        dialog.user["hobby"] = text
        await send_text(update, context, "Что тебе НЕ нравится в людях?")
    elif dialog.counter == 4:
        dialog.user["annoys"] = text
        await send_text(update, context, "Цели знакомства?")
    elif dialog.counter == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("profile")
        user_info = dialog_user_info_to_str(dialog.user)

        my_message = await send_text(update, context, "ChatGPT🧠 генерирует твой профиль...")
        answer = await chatgpt.send_question(prompt, user_info)
        await my_message.edit_text(answer)

async def opener(update, context):
    dialog.mode = "opener"


    text = load_message("opener")
    await send_photo(update, context, "opener")
    await send_text(update, context, text)

    dialog.user.clear()
    dialog.counter = 0
    await send_text(update, context, "Имя девушки?")

async def opener_dialog(update, context):
    text = update.message.text
    dialog.counter += 1

    if dialog.counter == 1:
        dialog.user["name"] = text
        await send_text(update, context, "Сколько ей лет?")
    elif dialog.counter == 2:
        dialog.user["age"] = text
        await send_text(update, context, "Оцените ее внешность: 1-10 баллов?")
    elif dialog.counter == 3:
        dialog.user["handsome"] = text
        await send_text(update, context, "Кем она работает?")
    elif dialog.counter == 4:
        dialog.user["occupation"] = text
        await send_text(update, context, "Цель знакомства?")
    elif dialog.counter == 5:
        dialog.user["goals"] = text
        prompt = load_prompt("opener")
        user_info = dialog_user_info_to_str(dialog.user)

        answer = await chatgpt.send_question(prompt, user_info)
        await send_text(update, context, answer)

async def hello(update, context):
    if dialog.mode == "gpt":
        await gpt_dialog(update, context)
    if dialog.mode == "date":
        await date_dialog(update, context)
    if dialog.mode == "message":
        await message_dialog(update, context)
    if dialog.mode == "profile":
        await profile_dialog(update, context)
    if dialog.mode == "opener":
        await opener_dialog(update, context)
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
dialog.list = []
dialog.counter = 0
dialog.user = {}

chatgpt = ChatGptService(token="gpt:EG44JHCgWRZcE28XEIsgJFkblB3TKFPdeHKs9DxUsueSBurd")

app = ApplicationBuilder().token("7442085622:AAEMZEDduTPxq00E-3HD1YXB1Y98dZw-EW0").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("gpt", gpt))
app.add_handler(CommandHandler("date", date))
app.add_handler(CommandHandler("message", message))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("opener", opener))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))

app.add_handler(CallbackQueryHandler(date_button, pattern="^date.*"))
app.add_handler(CallbackQueryHandler(message_button, pattern="^message.*"))
app.add_handler(CallbackQueryHandler(hello_button))
app.run_polling()
