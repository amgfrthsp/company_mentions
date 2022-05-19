"""
Extractor find mentions of companies and brands in differents media and store them in database.
"""

import asyncio
import logging

from extractors import meduza_extractor, twitter_extractor
from extractor import logic

# define logging format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    """
    Iterate over all extractors find last mentions in media.
    """
    await logic.initialize_database()

    extractors = [twitter_extractor, meduza_extractor]
    for extractor in extractors:
        await logic.extract_last_mentions(extractor)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())


if __name__ == '__main__':
    main()
