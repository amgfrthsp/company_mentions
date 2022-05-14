import logging

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import Table
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy import types
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

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
    company_id = Column(Integer)
    url = Column(String)
    title = Column(String)
    timestamp = Column(Integer)
    content = Column(String)
    type = Column(types.Enum)
    verdict = Column(types.JSON)
    is_sent = Column(types.BOOLEAN)

    def __repr__(self):
        return f"Mention: id={self.id!r}, title={self.title!r}"


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def get_engine():
    try:
        # +aiosqlite
        engine = create_async_engine('sqlite+aiosqlite:///database.db')
        logging.info("Database engine connected")
        return engine
    except:
        logging.error("Database error")


async def find_or_create_user(session, user_id: int) -> User:
    # .join(Company)
    stmt = select(User).where(User.telegram_user_id == user_id)
    user_db = (await session.scalars(stmt)).one_or_none()
    if user_db:
        logging.info(f"User {user_id} found in users database")
        return user_db

    new_user = User(telegram_user_id=user_id)
    session.add(new_user)
    logging.info(f"User {user_id} added to users database")
    return new_user


async def find_or_create_company(session, company_name: str) -> Company:
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


async def add_mention(session, mention: Mention):
    session.add(mention)
    logging.info(f"Mention {mention.title} added to mentions database")