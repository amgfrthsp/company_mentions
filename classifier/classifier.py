import asyncio
import logging

import logic
from models import Mention, MentionTypes
import dostoevsky_classifier, vader_classifier

# define logging format
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def async_main():
    await logic.initialize_database()
    mentions = await logic.get_unclassified_mentions()
    news = list(filter(lambda mention: mention.type == MentionTypes.NEWS, mentions))
    social_media_posts = list(filter(lambda mention: mention.type == MentionTypes.POST, mentions))

    classified_mentions = []
    classified_mentions.extend(dostoevsky_classifier.classify(news))
    classified_mentions.extend(vader_classifier.classify(social_media_posts))

    await logic.store_classified_mentions(classified_mentions)

if __name__ == '__main__':
    logging.info("START")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_main())
