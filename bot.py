from pyrogram import Client, filters
import requests
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем переменные окружения
TOKEN = os.getenv("TOKEN")  # Токен вашего бота
API_ID = int(os.getenv("API_ID", 12345))  # API ID от my.telegram.org
API_HASH = os.getenv("API_HASH")  # API Hash от my.telegram.org

# Инициализация клиента Pyrogram
app = Client("tinyurl_bot", bot_token=TOKEN, api_id=API_ID, api_hash=API_HASH)

# Функция для сокращения ссылки через TinyURL
def shorten_url(url):
    try:
        response = requests.get(f"http://tinyurl.com/api-create.php?url={url}")
        if response.status_code == 200:
            return response.text  # Возвращаем сокращённую ссылку
        else:
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# Обработчик команды /start
@app.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    await message.reply_text(
        "Привет! Я бот для сокращения ссылок через TinyURL.\n"
        "Просто отправь мне длинную ссылку, и я верну её сокращённую версию.",
        reply_to_message_id=message.id
    )

# Обработчик для сокращения ссылок
@app.on_message(filters.private & filters.regex("http|https"))
async def handle_url(client, message):
    URL = message.text
    print(f"Received URL: {URL}")  # Отладочное сообщение

    if not URL.startswith(("http://", "https://")):
        await message.reply_text(
            "Ошибка: Ссылка должна начинаться с http:// или https://.",
            reply_to_message_id=message.id
        )
        return

    short_url = shorten_url(URL)
    if short_url:
        await message.reply_text(
            f"Сокращённая ссылка: {short_url}",
            reply_to_message_id=message.id
        )
    else:
        await message.reply_text(
            "Ошибка: Не удалось сократить ссылку. Попробуйте ещё раз.",
            reply_to_message_id=message.id
        )

# Запуск бота
app.run()