import asyncio
import sys

from aiogram import Bot

import config
from handlers import router_dp


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    print("Bot ishga tushdi! ✅")
    sys.stdout.flush()
    await router_dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
