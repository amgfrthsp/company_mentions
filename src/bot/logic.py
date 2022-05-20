from itertools import groupby
from operator import attrgetter

from database import utils, tables
from models import SentimentTypes, CompanyNotifications, NotificationContent, MentionTypes


async def initialize_database():
    await utils.initialize()


async def start_bot(telegram_user_id: int):
    async with utils.Session() as session:
        await utils.get_or_create_user(session, telegram_user_id)
        await session.commit()


async def subscribe(telegram_user_id: int, company_name: str):
    async with utils.Session() as session:
        user = await utils.get_or_create_user(session, telegram_user_id)
        company = await utils.get_or_create_company(session, company_name)
        await utils.create_subscription(user, company)
        await session.commit()


async def unsubscribe(telegram_user_id: int, company_name: str):
    async with utils.Session() as session:
        user = await utils.get_or_create_user(session, telegram_user_id)
        company = await utils.get_or_create_company(session, company_name)
        await utils.delete_subscription(user, company)
        await session.commit()


async def get_subscriptions(telegram_user_id: int) -> list[str]:
    async with utils.Session() as session:
        user = await utils.get_or_create_user(session, telegram_user_id)
        subscriptions = [company.name for company in user.companies]
        await session.commit()
    return subscriptions


def get_sentiment(verdict: tables.Verdict) -> SentimentTypes:
    if verdict.negative and verdict.negative > 0.15:
        return SentimentTypes.NEGATIVE
    if verdict.positive and verdict.positive > 0.15:
        return SentimentTypes.POSITIVE
    return SentimentTypes.NEUTRAL


async def get_company_notification(company: tables.Company, company_mentions: list[tables.Mention]) -> CompanyNotifications:
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
    async with utils.Session() as session:
        mentions = await utils.get_all_unsent_mentions_sorted_by_company(session)

        notifications = []
        for company, company_mentions in groupby(mentions, attrgetter('company')):
            notifications.append(await get_company_notification(company, company_mentions))
        await session.commit()
    return notifications
