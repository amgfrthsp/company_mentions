import translators as ts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
limit_of_length = 5000 - 5


def classifyPubs(pubs):
    messages = [ts.google(pub["content"][:limit_of_length]) for pub in pubs]
    classified = [analyzer.polarity_scores(message) for message in messages]
    return classified
