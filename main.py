#!/usr/bin/env python3

import datetime
import logging

from dateutil import tz
from punbot.gme_api import get_prices
from punbot.sqlite import SQLite
from pydantic import Field
from pydantic_settings import BaseSettings
from telegram import constants
from telegram.ext import Application, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class Settings(BaseSettings):
    CHAT_ID: int = Field(default=...)
    TELEGRAM_TOKEN: str = Field(default=...)
    DB_PATH: str = Field(default="/data/prices.db")


settings = Settings()


async def job_handler(context: ContextTypes.DEFAULT_TYPE):
    sqlite = SQLite(settings.DB_PATH)
    sqlite.create_table()

    new_prices = get_prices()
    sqlite.insert(new_prices)
    avg_prices = sqlite.get_n_average(30)

    message = f"""
Indici del mercato elettrico e del gas (30d avg):
{avg_prices.str_with_diff(new_prices)}

Indici del mercato elettrico e del gas (new):
{new_prices}
    """

    await context.bot.send_message(
        chat_id=settings.CHAT_ID,
        text=message,
        disable_web_page_preview=True,
        disable_notification=True,
        parse_mode=constants.ParseMode.HTML,
    )


def main() -> int:
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()

    application.job_queue.run_daily(
        job_handler,
        time=datetime.time(hour=8, minute=0, second=0, tzinfo=tz.gettz("Europe/Rome")),
    )
    application.run_polling()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
