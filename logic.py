import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

engine = None
Session = sessionmaker(class_=AsyncSession)


async def initialize_database():
    global engine
    engine = db.get_engine()
    await db.create_tables(engine)

    Session.configure(bind=engine)


async def start_bot(telegram_user_id: int):
    async with Session() as session:
        await db.find_or_create_user(session, telegram_user_id)
        await session.commit()


async def subscribe(telegram_user_id: int, company_name: str):
    async with Session() as session:
        user = await db.find_or_create_user(session, telegram_user_id)
        company = await db.find_or_create_company(session, company_name)
        await db.create_subscription(user, company)
        await session.commit()


async def unsubscribe(telegram_user_id: int, company_name: str):
    async with Session() as session:
        user = await db.find_or_create_user(session, telegram_user_id)
        company = await db.find_or_create_company(session, company_name)
        await db.delete_subscription(user, company)
        await session.commit()


async def get_subscriptions(telegram_user_id: int) -> list:
    async with Session() as session:
        user = await db.find_or_create_user(session, telegram_user_id)
        subscriptions = [company.name for company in await db.get_subscriptions(user)]
        await session.commit()
    return subscriptions


async def add_mention(mention: db.Mention) -> db.Mention:
    async with Session() as session:
        await db.add_mention(session, mention)
        await session.commit()
    return mention
