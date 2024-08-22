
from termcolor import cprint
import os
import asyncio
import tg
import ds

TG_BOT_KEY = os.environ.get("TG_BOT_KEY")
DS_BOT_KEY = os.environ.get("DS_BOT_KEY")

if __name__ == "__main__":
    # tg_bot = tg.TGBot()
    # tg_bot.token = TG_BOT_KEY
    # tg_bot.init_bot()
    # asyncio.run(tg_bot.run())
    # cprint("TG BOT started")

    discord_bot = ds.DSBot(DS_BOT_KEY)
    asyncio.run(discord_bot.start())
    cprint("DS BOT started")