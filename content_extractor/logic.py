import db


async def initialize_database():
    await db.initialize()


async def get_companies() -> list:
    async with db.Session() as session:
        subscriptions = [company.name for company in await db.get_all_companies(session)]
    return subscriptions


async def store_mentions(mentions: list):
    async with db.Session() as session:
        for mention in mentions:
            company = await db.find_or_create_company(session, mention.company_name)
            await db.create_mention(session,
                                    company_id=company.id,
                                    title=mention.title,
                                    content=mention.content,
                                    url=mention.url,
                                    timestamp=mention.timestamp,
                                    type=mention.type)
        await session.commit()
