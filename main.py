#!/usr/bin/env python3

import asyncio
import contextlib
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings
from telegram import Bot, constants
from telegram.error import BadRequest

from punbot.gme_api import get_prices
from punbot.sqlite import SQLite

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__file__)


class Settings(BaseSettings):
    CHAT_ID: int = Field(default=...)
    TELEGRAM_TOKEN: str = Field(default=...)
    DB_PATH: str = Field(default="/data/prices.db")


async def job_handler(bot: Bot, chat_id: str, db: SQLite) -> None:
    new_prices = get_prices()
    db.insert(new_prices)
    avg_prices = db.get_n_average(30)

    message = f"""
Indici del mercato elettrico e del gas (30d avg):
{avg_prices.str_with_diff(new_prices)}

Indici del mercato elettrico e del gas (new):
{new_prices}
    """

    while True:
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=message,
                disable_web_page_preview=True,
                disable_notification=True,
                parse_mode=constants.ParseMode.HTML,
            )
            break
        except BadRequest as re:
            logger.error("An error occurred while sending the error message", exc_info=re)
            await asyncio.sleep(5)


async def main() -> None:
    load_dotenv()
    settings = Settings()

    scheduler = AsyncIOScheduler()

    sqlite = SQLite(settings.DB_PATH)
    sqlite.create_table()

    async with Bot(settings.TELEGRAM_TOKEN) as bot:
        scheduler.add_job(
            job_handler,
            kwargs={"bot": bot, "chat_id": settings.CHAT_ID, "db": sqlite},
            trigger="cron",
            hour=8,
            minute=0,
            timezone="Europe/Rome",
        )
        scheduler.start()
        while True:
            await asyncio.sleep(1000)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        asyncio.run(main())
