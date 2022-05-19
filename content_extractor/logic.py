from sqlalchemy.ext.asyncio import AsyncSession

from database import functions, tables
from models import Mention


async def initialize_database():
    await functions.initialize()


async def create_mentions(session: AsyncSession, company: tables.Company, mentions: list[Mention]):
    for mention in mentions:
        await functions.create_mention(session,
                                company_id=company.id,
                                title=mention.title,
                                content=mention.content,
                                url=mention.url,
                                timestamp=mention.timestamp,
                                type=mention.type)


async def extract_last_mentions(extractor):
    async with functions.Session() as session:
        companies = await functions.get_all_companies(session)
        for company in companies:
            mentions = extractor.get_last_mentions(company.name)
            await create_mentions(session, company, mentions)
        await session.commit()
