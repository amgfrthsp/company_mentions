import asyncio
import logging

import twitter_getter
import meduza_getter
from content_extractor import logic

# define logging format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    await logic.initialize_database()
    companies = await logic.get_companies()
    for company_name in companies:
        mentions = []
        mentions.extend(twitter_getter.get_last_mentions(company_name))
        mentions.extend(meduza_getter.get_last_mentions(company_name))
        await logic.store_mentions(mentions)


if __name__ == '__main__':
    logging.info("START")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
