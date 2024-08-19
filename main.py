
from termcolor import cprint
import tg
import os
import asyncio

cprint("MODULE STARTED", "green")

TG_BOT_KEY = os.environ.get("TG_BOT_KEY")

async def main():
    tgBot = tg.TelegramBot(TG_BOT_KEY)
    await tgBot.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())