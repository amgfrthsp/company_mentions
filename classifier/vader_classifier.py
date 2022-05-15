import translators as ts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from models import ClassifiedMention

analyzer = SentimentIntensityAnalyzer()
limit_of_length = 5000 - 5


def classify(mentions):
    messages = [ts.google(mention.content[:limit_of_length]) for mention in mentions]
    verdicts = [analyzer.polarity_scores(message) for message in messages]

    classified_mentions = []

    for i in range(0, len(verdicts)):
        classified_mentions.append(ClassifiedMention(
            id=0,
            base_mention_id=mentions[i].id,
            positive=verdicts[i].get("pos"),
            neutral=verdicts[i].get("neu"),
            negative=verdicts[i].get("neg")))

    return classified_mentions
