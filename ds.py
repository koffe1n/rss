import logging
from datetime import datetime, timezone, timedelta
from termcolor import cprint
import asyncio

import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import db
import rss
import utils

class DSBot:
    def __init__(self, token):
        intents = discord.Intents.default()
        intents.message_content = True

        self.token = token
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
        self.db = db.DB()
        self._setup_logging()
        self._setup_handlers()
        self._init_db()
        self.last_refresh = datetime.now(timezone.utc) - timedelta(hours=6)
        self.source = "discord"
        self.channel_id = None

    def _init_db(self):
        self.db.connect()
        self.db.prepare()

    def _setup_logging(self):
        logging.basicConfig(level=logging.INFO)

    def _setup_handlers(self):
        @self.bot.command(name='ping')
        async def ping(ctx):
            if self.channel_id == None:
                self.channel_id = ctx.channel.id
            await ctx.send("I'm still here")

        @self.bot.command(name='start')
        async def cmd_start(ctx):
            self.db.add_user(ctx.author.id, str(ctx.author), self.source)
            await ctx.send("Введите команду !subscribe <url> чтобы подписаться на рассылку")

        @self.bot.command(name='subscribe')
        async def subscribe(ctx, *rss_urls):
            for url in rss_urls:
                self.db.add_subscription(ctx.author.id, url)
                try:
                    title = rss.getRssTitle(url)
                except:
                    await ctx.send(f"Некорректная ссылка: {url}")
                    return
                if self.channel_id == None:
                    self.channel_id = ctx.channel.id
                await ctx.send(f"Вы подписаны на рассылку {title}")

        @self.bot.command(name='unsubscribe')
        async def unsubscribe(ctx, *rss_urls):
            for url in rss_urls:
                self.db.delete_subscription(ctx.author.id, url)
                title = rss.getRssTitle(url)
                await ctx.send(f"Вы отписались от рассылки {title}")

    async def send_scheduled_message(self):
        users = self.db.get_all_users_subscriptions(self.source)
        for user_id, url in users:
            feed = rss.getRssContent(url)
            for e in feed.entries:
                try:
                    if utils.convert_time(e.published) > self.last_refresh:
                        message = f"**{e.title}**\n\n{e.summary}\n\n{e.link}\n\n{e.published}"
                        channel = self.bot.get_channel(self.channel_id)
                        await channel.send(message)
                except Exception as e:
                    cprint(f"Ошибка отправки сообщения пользователю {user_id}: {e}")
        self.last_refresh = datetime.now(timezone.utc)

    def start_scheduler(self):
        self.scheduler.add_job(self.send_scheduled_message, 'interval', seconds=10)
        self.scheduler.start()

    async def start(self):
        self.start_scheduler()
        await self.bot.start(self.token)


