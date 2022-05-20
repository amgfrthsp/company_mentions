import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

import models
from database.tables import Base, User, Company, Mention

engine = None
Session = sessionmaker(class_=AsyncSession)


async def initialize():
    """
    Create all tables if they don't exist.
    """
    global engine
    engine = get_engine()
    await create_tables(engine)

    Session.configure(bind=engine)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Tables created")


def get_engine():
    """
    Do connection to SQLite database.
    """
    try:
        engine = create_async_engine('sqlite+aiosqlite:///database.db')
        logging.info("Database engine connected")
        return engine
    except Exception as e:
        raise Exception("Database error", e)


async def get_or_create_user(session: AsyncSession, user_id: int) -> User:
    """
    Return user with user_id in database. If it doesn't exist, create one.
    """
    stmt = select(User).where(User.telegram_user_id == user_id)
    user_db = (await session.scalars(stmt)).one_or_none()
    if user_db:
        logging.info(f"User {user_id} found in users database")
        return user_db

    new_user = User(telegram_user_id=user_id)
    session.add(new_user)
    logging.info(f"User {user_id} added to users database")
    return new_user


async def get_or_create_company(session: AsyncSession, company_name: str) -> Company:
    """
    Return company with company_name in database. If it doesn't exist, create one.
    """
    stmt = select(Company).where(Company.name == company_name)
    company_db = (await session.scalars(stmt)).one_or_none()
    if company_db:
        logging.info(f"Company {company_name} found in companies database")
        return company_db

    new_company = Company(name=company_name)
    session.add(new_company)
    logging.info(f"Company {company_name} added to companies database")
    return new_company


async def get_all_companies(session: AsyncSession) -> list[Company]:
    """
    Return list of all companies in database.
    """
    stmt = select(Company)
    companies = (await session.scalars(stmt)).all()
    logging.info(f"{len(companies)} companies returned")
    return companies


async def create_subscription(user: User, company: Company):
    """
    Create subscription between user and company. If already exists, raise exception.
    """
    if company in user.companies:
        raise Exception(f"Subscription {user.telegram_user_id}-{company.name} already exists")

    user.companies.append(company)
    logging.info(f"Association between {user.telegram_user_id} and {company.name} is added to association database")


async def delete_subscription(user: User, company: Company):
    """
    Delete subscription between user and company. If doesn't exist, raise exception.
    """
    if company not in user.companies:
        raise Exception(f"Subscription {user.telegram_user_id}-{company.name} does not exist")

    user.companies.remove(company)
    logging.info(f"Association between {user.telegram_user_id} and {company.name} is deleted from association database")


async def create_mention(session: AsyncSession,
                         company_id: int,
                         title: str,
                         content: str,
                         url: str,
                         timestamp: int,
                         type: models.MentionTypes):
    """
    Create mention of company with company_id with parameters. If already exists, do nothing.
    """
    stmt = select(Mention).where(Mention.url == url)
    mention = (await session.scalars(stmt)).one_or_none()
    if mention:
        raise Exception(f"Mention already exists")

    new_mention = Mention(
        company_id=company_id,
        title=title,
        content=content,
        url=url,
        timestamp=timestamp,
        type=type,
        is_sent=False
    )
    session.add(new_mention)


async def get_all_unsent_mentions_sorted_by_company(session: AsyncSession) -> list[Mention]:
    """
    Return list of unsent mentions ordered by company_id.
    """
    stmt = select(Mention).where(Mention.is_sent == False).order_by(Mention.company_id)
    unsent_mentions_db = (await session.scalars(stmt)).all()
    logging.info(f"{len(unsent_mentions_db)} unsent mentions returned")
    return unsent_mentions_db


async def get_unclassified_mentions(session: AsyncSession) -> list[Mention]:
    """
    Return list of all unclassified mentions in database.
    """
    stmt = select(Mention).where(Mention.verdict == None)
    mentions = (await session.scalars(stmt)).all()
    logging.info(f"{len(mentions)} unclassified mentions returned")
    return mentions
