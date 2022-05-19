import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Table, UniqueConstraint, Column, ForeignKey, Integer, String, Boolean, Enum, Float
from sqlalchemy import select
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
    __table_args__ = (UniqueConstraint("telegram_user_id", name="unique_telegram_user_id"),)

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer)
    companies = relationship(
        "Company",
        secondary=users_companies_association_table,
        back_populates="users",
        lazy="selectin"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, telegram_user_id={self.telegram_user_id!r})"


class Company(Base):
    """
    Define table companies(id INTEGER primary_key, name VARCHAR)
    """
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint("name", name="unique_name"),)

    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship(
        "User",
        secondary=users_companies_association_table,
        back_populates="companies",
        lazy="selectin"
    )

    mentions = relationship(
        "Mention",
        back_populates="company",
        uselist=False
    )

    def __repr__(self):
        return f"Company(id={self.id!r}, name={self.name!r})"


class Mention(Base):
    __tablename__ = "mentions"
    __table_args__ = (UniqueConstraint("url", name="unique_url"),)

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    title = Column(String)
    content = Column(String)
    url = Column(String)
    timestamp = Column(Integer)
    type = Column(Enum(models.MentionTypes))
    is_sent = Column(Boolean)

    company = relationship(
        "Company",
        back_populates="mentions",
        lazy="selectin"
    )

    verdict = relationship(
        "Verdict",
        # back_populates="base_mention",
        lazy="selectin",
        uselist=False)

    def __repr__(self):
        return f"Mention: id={self.id!r}, company={self.company.name!r}, title={self.title!r}"


class Verdict(Base):
    __tablename__ = "verdicts"
    id = Column(Integer, ForeignKey("mentions.id"), primary_key=True)
    positive = Column(Float)
    neutral = Column(Float)
    negative = Column(Float)

    mention = relationship(
        "Mention",
        back_populates="verdict",
        lazy="selectin",
    )

    def __repr__(self):
        return f"Classified mention: id={self.id!r}, ({self.positive!r}, {self.neutral!r}, {self.negative!r})"


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
        raise Exception(f"Subscription {user.telegram_user_id}-{company.name} already exists")

    user.companies.append(company)
    logging.info(f"Association between {user.telegram_user_id} and {company.name} is added to association database")


async def delete_subscription(user: User, company: Company):
    if company not in user.companies:
        raise Exception(f"Subscription {user.telegram_user_id}-{company.name} does not exist")

    user.companies.remove(company)
    logging.info(f"Association between {user.telegram_user_id} and {company.name} is deleted from association database")


async def get_all_unsent_mentions_sorted_by_company(session: AsyncSession) -> list[Mention]:
    stmt = select(Mention).where(Mention.is_sent == False).order_by(Mention.company_id)
    unsent_mentions_db = (await session.scalars(stmt)).all()
    logging.info(f"{len(unsent_mentions_db)} unsent mentions returned")
    return unsent_mentions_db


async def get_all_companies(session: AsyncSession) -> list:
    stmt = select(Company)
    companies = (await session.scalars(stmt)).all()
    logging.info(f"{len(companies)} companies returned")
    return companies


async def create_mention(session: AsyncSession,
                         company_id: int,
                         title: str,
                         content: str,
                         url: str,
                         timestamp: int,
                         type: models.MentionTypes,
                         is_sent=False):
    stmt = select(Mention).where(Mention.url == url)
    mention = (await session.scalars(stmt)).one_or_none()
    if mention:
        logging.info(f"Mention {url} already exists")
        return

    new_mention = Mention(
        company_id=company_id,
        title=title,
        content=content,
        url=url,
        timestamp=timestamp,
        type=type,
        is_sent=is_sent
    )
    session.add(new_mention)
    logging.info(f"Mention of {company_id} added to mentions database")


async def get_unclassified_mentions(session: AsyncSession) -> list[Mention]:
    stmt = select(Mention).where(Mention.verdict == None)
    mentions = (await session.scalars(stmt)).all()
    logging.info(f"{len(mentions)} unclassified mentions returned")
    return mentions
