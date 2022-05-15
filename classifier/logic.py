import db
import models

from models import Mention


async def initialize_database():
    await db.initialize()


async def get_unclassified_mentions() -> list:
    async with db.Session() as session:
        unclassified = await db.get_unclassified_mentions(session)
        mentions = [Mention(company_name=mention.company_name,
                            title=mention.title,
                            content=mention.content,
                            url=mention.url,
                            timestamp=mention.timestamp,
                            type=mention.type) for mention in unclassified]
        await session.commit()
    return mentions


# async def store_classified_mentions(mentions: list):
#     async with db.Session() as session:
#         await db.add_classified_mentions(session, mentions)
#         await session.commit()


async def store_classified_mentions(mentions: list[models.ClassifiedMention]):
    async with db.Session() as session:
        for mention in mentions:
            unclassified_mention = await db.get_unclassified_mention(session, mention.url)
            await db.add_classified_mention(unclassified_mention, mention.positive, mention.neutral, mention.negative)
        await session.commit()