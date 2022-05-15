import translators as ts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
limit_of_length = 5000 - 5


def classify(mentions):
    messages = [ts.google(mention.content[:limit_of_length]) for mention in mentions]
    verdicts = [analyzer.polarity_scores(message) for message in messages]
    for i in range(0, len(verdicts)):
        mentions[i].verdict = {"negative": verdicts[i].get("neg"),
                               "positive": verdicts[i].get("pos"),
                               "neutral": verdicts[i].get("neu")}

    return mentions
