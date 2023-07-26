#!/usr/bin/env python3

import os
import logging
import datetime
from dateutil import tz
from telegram import constants
from telegram.ext import Application, ContextTypes
from lib.gme_api import get_indexes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

CHAT_ID = int(os.environ["CHAT_ID"])


async def job_handler(context: ContextTypes.DEFAULT_TYPE):
    indexes = get_indexes()

    message = f"""
Indici del mercato elettrico e del gas:
<b>PUN</b>: {indexes["pun"]:.5f} €/kWh
<b>MGP Gas</b>: {indexes["mgp_gas"]:.5f} €/Smc
    """

    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=message,
        disable_web_page_preview=True,
        disable_notification=True,
        parse_mode=constants.ParseMode.HTML,
    )


if __name__ == "__main__":
    token = os.environ["TELEGRAM_TOKEN"]
    application = Application.builder().token(token).build()

    application.job_queue.run_daily(
        job_handler,
        time=datetime.time(hour=8, minute=0, second=0, tzinfo=tz.gettz("Europe/Rome")),
    )

    application.run_polling()
