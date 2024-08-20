import asyncio
import logging
import os
from termcolor import cprint

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import db

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
token = os.environ.get("TG_BOT_KEY")
bot = Bot(token=token)
scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

# Диспетчер
dp = Dispatcher()
db = db.DB()
db.connect()
db.prepare()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(Command('subscribe'))
async def subscribe(message: types.Message):
    rss_list = message.text.split(" ")[1:]
    for url in rss_list:
        db.add_subscription(message.from_user.id, url)
    await message.reply("Вы подписаны на рассылку!")

# Функция, которая будет выполняться по расписанию
async def send_scheduled_message():
    users = db.get_users_subscriptions()
    for user_id, url in users:
        try:
            cprint(user_id, 'green')
            await bot.send_message(user_id, f"Это регулярная рассылка! {url}")
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

# Запуск процесса поллинга новых апдейтов
async def main():
    scheduler.add_job(send_scheduled_message, 'interval', seconds=3)
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())