from sqlalchemy.ext.asyncio import AsyncSession

import db
from models import Mention


async def initialize_database():
    await db.initialize()


async def create_mentions(session: AsyncSession, company: db.Company, mentions: list[Mention]):
    for mention in mentions:
        await db.create_mention(session,
                                company_id=company.id,
                                title=mention.title,
                                content=mention.content,
                                url=mention.url,
                                timestamp=mention.timestamp,
                                type=mention.type)


async def extract_last_mentions(extractor):
    async with db.Session() as session:
        companies = await db.get_all_companies(session)
        for company in companies:
            mentions = extractor.get_last_mentions(company.name)
            await create_mentions(session, company, mentions)
        await session.commit()
