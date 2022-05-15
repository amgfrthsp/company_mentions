import db

from models import Mention


async def initialize_database():
    await db.initialize()


async def get_unclassified_mentions() -> list:
    async with db.Session() as session:
        mentions = [Mention(id=mention.id,
                            company_name=mention.company_name,
                            title=mention.title,
                            content=mention.content,
                            url=mention.url,
                            timestamp=mention.timestamp,
                            type=mention.type,
                            verdict=mention.verdict) for mention in await db.get_unclassified_mentions(session)]
        await session.commit()
    return mentions


async def store_classified_mentions(mentions: list):
    async with db.Session() as session:
        await db.add_classified_mentions(session, mentions)
        await session.commit()
