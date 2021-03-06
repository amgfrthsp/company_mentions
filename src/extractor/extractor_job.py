"""
Extractor find mentions of companies and brands in different media and store them in database.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from decouple import config
import sys
import asyncio
import logging
import os

sys.path.append(".")

from extractor.extractors import meduza_extractor, twitter_extractor, panorama_extractor
import extractor.logic as logic

LOGS_PATH = config('LOGS_PATH', default=os.path.join(os.pardir, "logs"))
logging.basicConfig(
    filename=os.path.join(LOGS_PATH, "extractor.log"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    """
    Iterate over all extractors find last mentions in media.
    """
    await logic.initialize_database()

    logging.info("started extracting mentions...")
    extractors = [twitter_extractor, meduza_extractor, panorama_extractor]
    for extractor in extractors:
        logging.info(f"started monitoring {extractor.NAME}...")
        await logic.extract_last_mentions(extractor)
        logging.info(f"finished monitoring {extractor.NAME}")
    logging.info("finished extracting mentions")


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
