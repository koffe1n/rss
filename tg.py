import telebot
from termcolor import cprint
import time
import rss

import asyncio
import schedule

import db

class TelegramBot:
    def __init__(self, key):
        self.key = key
        self.bot=telebot.TeleBot(key)
        self.scheduler = schedule.Scheduler
        self.db = db.DB
    
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message,"Check check")

        @self.bot.message_handler(commands=['add_feed'])
        def add_feed(message):
            rss_list = message.text.split(" ")[1:]
            for r in rss_list:
                self.db.add_subscription(self.db, message.from_user.id, r)
                # self.scheduler.add_job(researchRss, "interval", seconds=2, args=(self.bot, message.from_user.id, r))
            if len(rss_list) > 1:
                reply = "Лента добавлена"
            else:
                reply = "Ленты добавлены"
            self.bot.reply_to(message,reply)

        @self.bot.message_handler(commands=['remove_feed'])
        def remove_feed(message):
            rssList = message.text.split(" ")[1:]
            if len(rssList) > 1:
                reply = "Лента удалена из подписок"
            else:
                reply = "Ленты удалены из подписок"
            self.bot.reply_to(message,reply)

    def start(self):
        cprint("TG bot started", 'blue')
        try:
            self.db.connect(self.db)
            self.db.prepare(self.db)
        except Exception as e:
            cprint('ошибка при старте базы данных', 'red')
            print(e)
        
        schedule.every(3).seconds.do(lambda: asyncio.create_task(sendRss(self.bot)))
        asyncio.create_task(asyncio.to_thread(run_scheduler))
        self.bot.infinity_polling()

    async def sendMessage(self, user_id, message):
        self.bot.send_message(user_id, message)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

async def sendRss(bot):
    a = db.DB.get_users_subscriptions(db)
    for (user_id, url) in a:
        reply = rss.getRssContent(url)
        try:
            await bot.send_message(user_id, reply)
        except Exception as e:
            print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
