import translators as ts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from models import ClassifiedMention

analyzer = SentimentIntensityAnalyzer()
limit_of_length = 5000 - 5


def classify(mentions):
    messages = [ts.google(mention.content[:limit_of_length]) for mention in mentions]
    verdicts = [analyzer.polarity_scores(message) for message in messages]

    classified_mentions = []

    for i, verdict in enumerate(verdicts):
        classified_mentions.append(ClassifiedMention(
            url=mentions[i].url,
            positive=verdict.get("positive"),
            neutral=verdict.get("neutral"),
            negative=verdict.get("negative")))

    return classified_mentions
