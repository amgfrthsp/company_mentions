"""
Classifier analyze mentions of companies and brands in different media and store verdict into database.
"""
import os
import asyncio
import logging
import sys
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

sys.path.append(".")

import classifier.logic as logic


# define logging format
LOGS_PATH = config('LOGS_PATH', default=os.path.join(os.pardir, "logs"))
logging.basicConfig(
    filename=os.path.join(LOGS_PATH, "classifier.log"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    await logic.initialize_database()

    logging.info("started classifying...")
    await logic.classify_all()
    logging.info("finished classifying...")


def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(async_main, 'interval', minutes=20)
    scheduler.start()

    try:
        loop = asyncio.get_event_loop()
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
