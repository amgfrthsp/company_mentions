from itertools import groupby
from operator import attrgetter

import db
from models import SentimentTypes, CompanyNotifications, NotificationContent, MentionTypes


async def initialize_database():
    await db.initialize()


async def start_bot(telegram_user_id: int):
    async with db.Session() as session:
        await db.get_or_create_user(session, telegram_user_id)
        await session.commit()


async def subscribe(telegram_user_id: int, company_name: str):
    async with db.Session() as session:
        user = await db.get_or_create_user(session, telegram_user_id)
        company = await db.get_or_create_company(session, company_name)
        await db.create_subscription(user, company)
        await session.commit()


async def unsubscribe(telegram_user_id: int, company_name: str):
    async with db.Session() as session:
        user = await db.get_or_create_user(session, telegram_user_id)
        company = await db.get_or_create_company(session, company_name)
        await db.delete_subscription(user, company)
        await session.commit()


async def get_subscriptions(telegram_user_id: int) -> list[str]:
    async with db.Session() as session:
        user = await db.get_or_create_user(session, telegram_user_id)
        subscriptions = [company.name for company in user.companies]
        await session.commit()
    return subscriptions


def get_sentiment(verdict: db.Verdict) -> SentimentTypes:
    if verdict.negative and verdict.negative > 0.15:
        return SentimentTypes.NEGATIVE
    if verdict.positive and verdict.positive > 0.15:
        return SentimentTypes.POSITIVE
    return SentimentTypes.NEUTRAL


async def get_company_notification(company: db.Company, company_mentions: list[db.Mention]) -> CompanyNotifications:
    company_notification = CompanyNotifications(
        company_name=company.name,
        user_ids=[user.telegram_user_id for user in company.users]
    )

    for mention in company_mentions:
        notification_content = NotificationContent(
            title=mention.title,
            content=mention.content,
            url=mention.url,
            sentiment=get_sentiment(mention.verdict)
        )

        if mention.type == MentionTypes.NEWS:
            company_notification.news.append(notification_content)
        elif mention.type == MentionTypes.POST:
            company_notification.posts.append(notification_content)
        elif mention.type == MentionTypes.MEM:
            company_notification.mems.append(notification_content)

        mention.is_sent = True
    return company_notification


async def get_notifications() -> list[CompanyNotifications]:
    async with db.Session() as session:
        mentions = await db.get_all_unsent_mentions_sorted_by_company(session)

        notifications = []
        for company, company_mentions in groupby(mentions, attrgetter('company')):
            notifications.append(await get_company_notification(company, company_mentions))
        await session.commit()
    return notifications
