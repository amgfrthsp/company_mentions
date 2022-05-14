"""
Telegram-bot analizes mentions of companies and brands in media.
"""

import asyncio
import logging
import logic
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler


# define logging format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """
    Inform user about what this bot can do
    :param update:
    :param context:
    :return:
    """
    await logic.start(update.effective_user.id)
    await update.message.reply_text("Привет! Используй /subscribe <company> для получения уведомлений")


async def subscribe(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """
    Subscribe user to chosen company
    :param update:
    :param context:
    :return:
    """
    # args should contain the name of company
    if not context.args:
        await update.effective_message.reply_text("Используй /subscribe <company>")
        return
    company_name = ' '.join(context.args)

    try:
        await logic.subscribe(update.effective_user.id, company_name)
    except Exception as e:
        logging.exception(e)
        await update.message.reply_text(f"Ты уже подписан на {company_name}")
        return

    await update.message.reply_text(f"Ты подписался на {company_name}")


async def unsubscribe(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """
    Unsubscribe user from chosen company
    :param update:
    :param context:
    :return:
    """
    # args should contain the name of company
    if not context.args:
        await update.effective_message.reply_text("Используй /unsubscribe <company>")
        return
    company_name = ' '.join(context.args)

    try:
        await logic.unsubscribe(update.effective_user.id, company_name)
    except:
        await update.message.reply_text(f"Ты и так не подписан на {company_name}")
        return

    await update.message.reply_text(f"Ты отписался от {company_name}")


async def get_subscriptions(update: Update, context: CallbackContext.DEFAULT_TYPE):
    """
    List all subscriptions of user
    :param update:
    :param context:
    :return:
    """
    subscriptions = await logic.get_subscriptions(update.effective_user.id)
    subscriptions_text = '\n'.join(subscriptions)
    await update.message.reply_text(f"Ты подписан на:\n{subscriptions_text}")


async def async_main():
    await logic.initialize()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())

    application = ApplicationBuilder().token(token='TOKEN').build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe))
    application.add_handler(CommandHandler("get_subscriptions", get_subscriptions))
    application.run_polling()