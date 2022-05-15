import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Table, UniqueConstraint, Column, ForeignKey, Integer, String, Boolean, Enum
from sqlalchemy import select, types, update
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

import models

engine = None
Session = sessionmaker(class_=AsyncSession)


Base = declarative_base()

users_companies_association_table = Table('users_companies_association', Base.metadata,
                                          Column('user_id', ForeignKey('users.id'), primary_key=True),
                                          Column('company_id', ForeignKey('companies.id'), primary_key=True)
                                          )


class User(Base):
    """
    Define table users(id INTEGER primary_key, telegram_user_id INTEGER)
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer)
    companies = relationship(
        "Company",
        secondary=users_companies_association_table,
        back_populates="users",
        lazy="selectin")
    __table_args__ = (UniqueConstraint("telegram_user_id", name="unique_telegram_user_id"),)

    def __repr__(self):
        return f"User(id={self.id!r}, telegram_user_id={self.telegram_user_id!r})"


class Company(Base):
    """
    Define table companies(id INTEGER primary_key, name VARCHAR)
    """
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    users = relationship(
        "User",
        secondary=users_companies_association_table,
        back_populates="companies")
    __table_args__ = (UniqueConstraint("name", name="unique_name"),)

    def __repr__(self):
        return f"Company(id={self.id!r}, name={self.name!r})"


class Mention(Base):
    __tablename__ = "mentions"
    id = Column(Integer, primary_key=True)
    company_name = Column(String)
    title = Column(String)
    content = Column(String)
    url = Column(String)
    timestamp = Column(Integer)
    type = Column(Enum(models.MentionTypes))
    verdict = Column(types.JSON)
    is_sent = Column(Boolean)

    __table_args__ = (UniqueConstraint("url", name="unique_url"),)

    def __repr__(self):
        return f"Mention: id={self.id!r}, title={self.title!r}"


async def initialize():
    global engine
    engine = get_engine()
    await create_tables(engine)

    Session.configure(bind=engine)


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Tables created")


def get_engine():
    try:
        # +aiosqlite
        engine = create_async_engine('sqlite+aiosqlite:///database.db')
        logging.info("Database engine connected")
        return engine
    except:
        logging.error("Database error")


async def find_or_create_user(session: AsyncSession, user_id: int) -> User:
    stmt = select(User).where(User.telegram_user_id == user_id)
    user_db = (await session.scalars(stmt)).one_or_none()
    if user_db:
        logging.info(f"User {user_id} found in users database")
        return user_db

    new_user = User(telegram_user_id=user_id)
    session.add(new_user)
    logging.info(f"User {user_id} added to users database")
    return new_user


async def find_or_create_company(session: AsyncSession, company_name: str) -> Company:
    stmt = select(Company).where(Company.name == company_name)
    company_db = (await session.scalars(stmt)).one_or_none()
    if company_db:
        logging.info(f"Company {company_name} found in companies database")
        return company_db

    new_company = Company(name=company_name)
    session.add(new_company)
    logging.info(f"Company {company_name} added to companies database")
    return new_company


async def create_subscription(user: User, company: Company):
    if company in user.companies:
        raise f"Subscription {user.telegram_user_id}-{company.name} already exists"
    user.companies.append(company)
    logging.info(f"Association between {user.telegram_user_id} and {company.name} is added to association database")


async def delete_subscription(user: User, company: Company):
    if company not in user.companies:
        raise f"Subscription {user.telegram_user_id}-{company.name} does not exist"
    user.companies.remove(company)
    logging.info(f"Association between {user.telegram_user_id} and {company.name} is deleted from association database")


async def get_subscriptions(user: User) -> list:
    return user.companies


async def get_all_companies(session: AsyncSession) -> list:
    stmt = select(Company)
    companies = (await session.scalars(stmt)).all()
    logging.info("%d companies returned", len(companies))
    return companies


async def create_mention(session: AsyncSession,
                         company_name: str,
                         title: str,
                         content: str,
                         url: str,
                         timestamp: int,
                         type,
                         verdict=None,
                         is_sent=False):
    new_mention = Mention(
        company_name=company_name,
        title=title,
        content=content,
        url=url,
        timestamp=timestamp,
        type=type,
        verdict=verdict,
        is_sent=is_sent
    )
    session.add(new_mention)
    logging.info(f"Mention of {company_name} added to mentions database")


async def get_unclassified_mentions(session: AsyncSession) -> list:
    stmt = select(Mention).where(Mention.verdict == None)
    mentions = (await session.scalars(stmt)).all()
    logging.info("%d unclassified mentions returned", len(mentions))
    return mentions


async def add_classified_mentions(session: AsyncSession, mentions):
    for mention in mentions:
        stmt = update(Mention).where(Mention.id == mention.id).values(verdict=mention.verdict)
        await session.execute(stmt)
        await session.commit()
    logging.info("classified %d mentions", len(mentions))
