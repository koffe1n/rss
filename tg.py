import logging
from datetime import datetime, timezone
from termcolor import cprint

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import db
import rss
import utils

class TGBot:
    def __init__(self):
        self.token = None
        self.bot = None
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.dp = Dispatcher()
        self.db = db.DB()
        self._setup_logging()
        self._setup_handlers()
        self._init_db()
        self.last_refresh = datetime.now(timezone.utc)

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)

    def _setup_handlers(self):
        self.dp.message.register(self.cmd_start, Command("start"))
        self.dp.message.register(self.subscribe, Command('subscribe'))
        self.dp.message.register(self.unsubscribe, Command('unsubscribe'))

    def _init_db(self):
        self.db.connect()
        self.db.prepare()
    
    def init_bot(self):
        self.bot = Bot(token=self.token)

    async def cmd_start(self, message: types.Message):
        self.db.add_user(message.from_user.id, message.from_user.username)
        await message.answer("Hello!")

    async def subscribe(self, message: types.Message):
        rss_list = message.text.split(" ")[1:]
        for url in rss_list:
            self.db.add_subscription(message.from_user.id, url)
            title = rss.getRssTitle(url)
            await message.reply(f"Вы подписаны на рассылку {title}")

    async def unsubscribe(self, message: types.Message):
        rss_list = message.text.split(" ")[1:]
        for url in rss_list:
            self.db.delete_subscription(message.from_user.id, url)
            title = rss.getRssTitle(url)
            await message.reply(f"Вы отписались от рассылки {title}")

    async def send_scheduled_message(self):
        users = self.db.get_all_users_subscriptions()
        for user_id, url in users:
            feed = rss.getRssContent(url)
            for e in feed.entries:
                try:
                    if utils.convert_time(e.published) < self.last_refresh:
                        continue
                    message = as_list(
                        Bold(e.title),
                        e.summary,
                        e.link,
                        e.published,
                        sep="\n\n"
                    )
                    await self.bot.send_message(user_id, **message.as_kwargs())
                except Exception as e:
                    cprint(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
            self.last_refresh = datetime.now()

    async def run(self):
        self.scheduler.add_job(self.send_scheduled_message, 'interval', seconds=3)
        self.scheduler.start()
        await self.dp.start_polling(self.bot)


