import db
import logging
from models import Mention


async def initialize_database():
    await db.initialize()


async def get_companies() -> list:
    async with db.Session() as session:
        subscriptions = [company.name for company in await db.get_all_companies(session)]
        await session.commit()
    logging.info("Companies returned")
    return subscriptions


async def store_mentions(mentions: list[Mention]):
    async with db.Session() as session:
        for mention in mentions:
            await db.create_mention(session,
                                    company_name=mention.company_name,
                                    title=mention.title,
                                    content=mention.content,
                                    url=mention.url,
                                    timestamp=mention.timestamp,
                                    type=mention.type)
        await session.commit()
