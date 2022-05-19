import logging

import db
import models
from classifiers import dostoevsky_classifier, vader_classifier


async def initialize_database():
    await db.initialize()


async def classify(mention: db.Mention):
    if mention.type == models.MentionTypes.POST:
        verdict = vader_classifier.classify(mention.content)
    else:
        verdict = dostoevsky_classifier.classify(mention.content)
    mention.verdict = db.Verdict(
        positive=verdict.positive,
        neutral=verdict.neutral,
        negative=verdict.negative
    )


async def classify_all():
    async with db.Session() as session:
        unclassified_mentions_db = await db.get_unclassified_mentions(session)

        for mention_db in unclassified_mentions_db:
            await classify(mention_db)
            logging.info(f"{mention_db.id} is classified")

        logging.info(f"{len(unclassified_mentions_db)} mentions is classified")
        await session.commit()
