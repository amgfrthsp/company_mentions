import sys

sys.path.append("..")

import os
import asyncio
import logging
from decouple import config

import classifier.logic as logic

# define logging format
LOGS_PATH = config('LOGS_PATH', default=os.path.join(os.pardir, os.pardir, "logs"))
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


if __name__ == '__main__':
    working_directory = os.path.join(os.getcwd(), os.pardir, os.pardir)
    os.chdir(working_directory)
    main()
