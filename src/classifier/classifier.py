import os
import asyncio
import logging

import logic

# define logging format
logging.basicConfig(
    filename="../../logs/extractor.log",
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
