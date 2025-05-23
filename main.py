
import logging
from aiogram import Bot, Dispatcher, executor, types
import openai
import os

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот Seamech Assistant. Используй /ask или /docs.")

@dp.message_handler(commands=['ask'])
async def ask_gpt(message: types.Message):
    user_input = message.get_args()
    if not user_input:
        await message.reply("Напиши вопрос после команды /ask.")
        return
    await message.reply("Думаю...")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты помощник по судовой электромеханике."},
                {"role": "user", "content": user_input}
            ]
        )
        await message.reply(response['choices'][0]['message']['content'])
    except Exception as e:
        await message.reply(f"Ошибка: {e}")

@dp.message_handler(commands=['docs'])
async def send_docs(message: types.Message):
    await message.reply("""📚 ДОКУМЕНТАЦИЯ:
1. Схема электропитания двигателя [PDF]
2. Руководство по генератору [PDF]""")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

    
