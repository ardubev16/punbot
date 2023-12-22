#!/usr/bin/env python3

import os
import logging
import datetime
from dateutil import tz
from telegram import constants
from telegram.ext import Application, ContextTypes
from lib.gme_api import Indexes, get_indexes
from lib.util import average
import json

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

CHAT_ID = int(os.environ["CHAT_ID"])
INDEXES_FILE = "/data/indexes.json"


def get_old_indexes():
    if os.path.exists(INDEXES_FILE):
        with open(INDEXES_FILE, "r") as f:
            return json.load(f)
    return {
        "pun": [],
        "mgp_gas": [],
    }


def save_indexes(indexes):
    with open(INDEXES_FILE, "w") as f:
        json.dump(indexes, f)


def update_indexes(indexes, new_value: Indexes):
    indexes["pun"].append(new_value.pun)
    indexes["mgp_gas"].append(new_value.mgp_gas)
    if len(indexes) > 30:
        indexes["pun"].pop(0)
        indexes["mgp_gas"].pop(0)

    return indexes


async def job_handler(context: ContextTypes.DEFAULT_TYPE):
    indexes = get_indexes()
    old_indexes = get_old_indexes()
    new_indexes = update_indexes(old_indexes, indexes)
    save_indexes(new_indexes)

    pun_avg = average(new_indexes["pun"])
    mgp_gas_avg = average(new_indexes["mgp_gas"])
    avg_indexes = Indexes(pun_avg, mgp_gas_avg)

    message = f"""
Indici del mercato elettrico e del gas (30d avg):
{avg_indexes.str_avg(avg_indexes)}

Indici del mercato elettrico e del gas (new):
{indexes}
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
