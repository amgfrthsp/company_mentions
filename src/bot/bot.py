"""
Telegram-bot sent notifications with analyzed mentions of companies and brands.
"""

import asyncio
import datetime
import logging
import os

from decouple import config
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler

import logic
from models import SentimentTypes

TOKEN = config('TELEGRAM_BOT_TOKEN')
MAX_NEWS_LENGTH = 2000

LOGS_PATH = config('LOGS_PATH', default=os.path.join(os.pardir, os.pardir, "logs"))
logging.basicConfig(
    filename=os.path.join(LOGS_PATH, "bot.log"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, _context: CallbackContext.DEFAULT_TYPE):
    """
    Inform user about what this bot can do
    """
    message = f'''
Привет, {update.effective_user.name} 👋
Я уведомляю об интересных тебе компаниях и анализирую контекст. 

Используй эти команды для общения со мной:
/subscribe _company_ для того, чтобы подписаться на уведомления про компанию
/unsubscribe _company_ — отписаться
/get\_subscriptions — получить список всех подписок
/get\_last\_news _company_ — получить новости о компании за последнее время
/help чтобы еще раз получить это сообщение
'''
    await logic.start_bot(update.effective_chat.id)
    await update.message.reply_text(message, parse_mode="markdown")


async def subscribe(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """
    Subscribe user to chosen company.
    """
    # args should contain the name of company
    if not context.args:
        await update.effective_message.reply_text(f"Чтобы подписаться, напиши /subscribe _company_",
                                                  parse_mode="markdown")
        return

    company_name = ' '.join(context.args)

    try:
        await logic.subscribe(update.effective_chat.id, company_name)
    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(f"👀 У тебя уже есть подписка #{company_name}", parse_mode="markdown")
        return

    await update.message.reply_text(f"✅ Ты подписался на #{company_name}", parse_mode="markdown")


async def unsubscribe(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """
    Unsubscribe user from chosen company.
    """
    # args should contain the name of company
    if not context.args:
        await update.effective_message.reply_text("Чтобы отписаться, напиши /unsubscribe _company_",
                                                  parse_mode="markdown")
        return

    company_name = ' '.join(context.args)

    try:
        await logic.unsubscribe(update.effective_chat.id, company_name)
    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(f"👀 Ты и так не подписан на #{company_name}")
        return

    await update.message.reply_text(f"❎ Ты отписался от #{company_name}")


async def get_subscriptions(update: Update, _context: CallbackContext):
    """
    List all subscriptions of user.
    """
    subscriptions = await logic.get_subscriptions(update.effective_chat.id)
    if not subscriptions:
        await update.message.reply_text(f"❕ Ты ни на кого не подписан")
        return

    subscriptions_text = ''.join([f"#{subscription}\n" for subscription in subscriptions])
    await update.message.reply_text(f"❕ Ты подписан на:\n{subscriptions_text}")


async def get_sentiment_smile(sentiment: SentimentTypes) -> str:
    if sentiment == SentimentTypes.POSITIVE:
        return '🙂'
    elif sentiment == SentimentTypes.NEUTRAL:
        return '😐'
    elif sentiment == SentimentTypes.NEGATIVE:
        return '🙁'
    return '🤔'


async def get_news_text(news):
    max_news_length = MAX_NEWS_LENGTH // len(news)
    print(max_news_length)
    news_texts = []
    for new in news:
        title_text = f"*{new.title}*\n" if new.title else ""
        content_text = f"`{new.content[:max_news_length]}`[...]({new.url})\n" \
            if len(new.content) > max_news_length else \
            f"`{new.content}`\n[источник]({new.url})\n"
        news_texts.append(f"  {await get_sentiment_smile(new.sentiment)} {title_text}{content_text}")
    return ''.join(news_texts)


async def get_posts_text(posts):
    return ''.join([
        f"  {await get_sentiment_smile(post.sentiment)} _{post.content}_ [источник]({post.url})\n"
        for post in posts]
    )


async def get_mems_text(mems):
    return ''.join([
        f"  {await get_sentiment_smile(mem.sentiment)}\n{mem.content}\n[источник]({mem.url})\n"
        for mem in mems]
    )


async def send_notifications(context):
    """
    Notify followers about mentions.
    """
    notifications_by_companies = await logic.get_notifications()
    for company_notification in notifications_by_companies:
        news_text = ""
        posts_text = ""
        mems_text = ""

        if company_notification.news:
            news_text = f"📰 Новости:\n{await get_news_text(company_notification.news)}\n\n"
        if company_notification.posts:
            posts_text = f"💬 Посты:\n{await get_posts_text(company_notification.posts)}\n\n"
        if company_notification.mems:
            mems_text = f"🤣 Мемы:\n{await get_mems_text(company_notification.mems)}\n\n"

        text = f'''#{company_notification.company_name}\n\n{news_text}{posts_text}{mems_text}'''

        for user_id in company_notification.user_ids:
            await context.bot.send_message(chat_id=user_id, text=text, parse_mode="markdown")


async def async_main():
    await logic.initialize_database()


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())

    application = ApplicationBuilder().token(token=TOKEN).build()

    application.job_queue.run_repeating(send_notifications, interval=datetime.timedelta(hours=1), first=1)

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("get_subscriptions", get_subscriptions))
    application.run_polling()


if __name__ == '__main__':
    main()
