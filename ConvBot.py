import logging
import json
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Включаем логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

#Обрабатываем команду start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    logger.log(level=20,msg=update.message.text)
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Используй команду /convert для конвертации валют пример: /convert 100 USD to EUR"
    )

#обрабатываем команду about
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.log(level=20,msg=update.message.text)
    await update.message.reply_text(
        "Данный бот написан tg @voltako. Данный бот обеспечивает конвертацию валют по текущему курсу. Используется api с сайта https://currate.ru/. Частота обновления курса валют равна 1 часу. ")

#Обрабатываем команду help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.log(level=20,msg=update.message.text)
    await update.message.reply_text('''Данный бот конвертирует валюты с помощью команды /convert,пример /convert 100 EUR to RUB.
Команда /about выведет информацию о данном боте и авторе.
Команда /start начинает работу бота.
Команда /help выводит помощь.''')


#Добавляем обработчик всего чата
async def chat_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message.text.split()
    logger.log(level=20 ,msg=message)
    for word in message:
        if word == "Привет" or word == "привет":
            await update.message.reply_text("Привет, Пользователь!")
        if word == "Пока" or word == 'пока':
            await update.message.reply_text("Досвидания, Пользователь!")


#Функция конвертации валют
def convertation(value,first_currency,second_currency) -> int:
    apikey = "e0093ceb90844c10e9d86884266c5b3b"
    url =  "https://currate.ru/api/?get=rates&pairs="
    result = requests.get(url+first_currency+second_currency+"&key="+apikey)
    json_result = json.loads(result.content)
    currency = json_result["data"][first_currency+second_currency]
    value = float(value)*float(currency)
    return value

#Обрабатываем команду covert
async def convert(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.log(level=20,msg=update.message.text)
    msg =  update.message.text.split()
    value = msg[1]
    first_currency = msg[2]
    second_currency = msg[4]
    await update.message.reply_text("По текущему курсу валют "+value+" "+first_currency+" будет равно "+str(convertation(value,first_currency,second_currency))+" "+second_currency)


#Запуск программы
def main() -> None:
    #Вносим токен бота, добавляем обработчики команд, и обработчик чата
    application = Application.builder().token("Токен бота").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("convert", convert))
    application.add_handler(CommandHandler("about", about))

    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,chat_handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()