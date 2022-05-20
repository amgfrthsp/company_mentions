"""
Extractor find mentions of companies and brands in different media and store them in database.
"""

import asyncio
import logging

from extractors import meduza_extractor, twitter_extractor
import logic

# define logging format
logging.basicConfig(
    filename="extractor.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    """
    Iterate over all extractors find last mentions in media.
    """
    await logic.initialize_database()

    logging.info("started extracting mentions...")
    extractors = [twitter_extractor, meduza_extractor]
    for extractor in extractors:
        logging.info(f"started monitoring {extractor.NAME}...")
        await logic.extract_last_mentions(extractor)
        logging.info(f"finished monitoring {extractor.NAME}")
    logging.info("finished extracting mentions")


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


if __name__ == '__main__':
    main()
