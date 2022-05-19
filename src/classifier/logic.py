import logging


from classifiers import vader_classifier, dostoevsky_classifier
from src import models
from src.database import tables, functions


async def initialize_database():
    await functions.initialize()


async def classify(mention: tables.Mention):
    if mention.type == models.MentionTypes.POST:
        verdict = vader_classifier.classify(mention.content)
    else:
        verdict = dostoevsky_classifier.classify(mention.content)
    mention.verdict = tables.Verdict(
        positive=verdict.positive,
        neutral=verdict.neutral,
        negative=verdict.negative
    )


async def classify_all():
    async with functions.Session() as session:
        unclassified_mentions_db = await functions.get_unclassified_mentions(session)

        for mention_db in unclassified_mentions_db:
            await classify(mention_db)
            logging.info(f"{mention_db.id} is classified")

        logging.info(f"{len(unclassified_mentions_db)} mentions is classified")
        await session.commit()
