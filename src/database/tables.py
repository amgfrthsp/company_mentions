from sqlalchemy import Table, UniqueConstraint, Column, ForeignKey, Integer, String, Boolean, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

import models

Base = declarative_base()

# Define table subscriptions
subscriptions = Table('subscriptions', Base.metadata,
                      Column('user_id', ForeignKey('users.id'), primary_key=True),
                      Column('company_id', ForeignKey('companies.id'), primary_key=True)
                      )


class User(Base):
    """
    Define table users
    """
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("telegram_user_id", name="unique_telegram_user_id"),)

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer)

    companies = relationship(
        "Company",
        secondary=subscriptions,
        back_populates="users",
        lazy="selectin"
    )

    def __repr__(self):
        return f"User(id={self.id!r}, telegram_user_id={self.telegram_user_id!r})"


class Company(Base):
    """
    Define table companies
    """
    __tablename__ = "companies"
    __table_args__ = (UniqueConstraint("name", name="unique_name"),)

    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship(
        "User",
        secondary=subscriptions,
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
    """
    Define table mentions
    """
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
        lazy="selectin",
        uselist=False)

    def __repr__(self):
        return f"Mention: id={self.id!r}, company={self.company.name!r}, title={self.title!r}"


class Verdict(Base):
    """
    Define table Verdict
    """
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
