import logging

from sqlalchemy.ext.asyncio import AsyncSession

from database import utils, tables
from models import Mention

# define logging format
logging.basicConfig(
    filename="../../logs/classifier.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def initialize_database():
    await utils.initialize()


async def create_mentions(session: AsyncSession, company: tables.Company, mentions: list[Mention]):
    new_mentions_cnt = 0
    for mention in mentions:
        try:
            await utils.create_mention(session,
                                           company_id=company.id,
                                           title=mention.title,
                                           content=mention.content,
                                           url=mention.url,
                                           timestamp=mention.timestamp,
                                           type=mention.type)
            new_mentions_cnt += 1
        except Exception:
            pass

    logging.info(f"{new_mentions_cnt} new mentions of {company.name} added to database")


async def extract_last_mentions(extractor):
    async with utils.Session() as session:
        companies = await utils.get_all_companies(session)
        for company in companies:
            mentions = extractor.get_last_mentions(company.name)
            await create_mentions(session, company, mentions)
        await session.commit()
