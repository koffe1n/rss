
from termcolor import cprint
import tg
import os
import asyncio

cprint("MODULE STARTED", "green")

TG_BOT_KEY = os.environ.get("TG_BOT_KEY")

if __name__ == "__main__":
    tg_bot = tg.TGBot()
    tg_bot.token = TG_BOT_KEY
    tg_bot.init_bot()
    asyncio.run(tg_bot.run())