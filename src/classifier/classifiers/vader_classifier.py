import translators as ts
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from models import Verdict

analyzer = SentimentIntensityAnalyzer()
limit_of_length = 5000 - 5


def classify(message) -> Verdict:
    translated_message = ts.google(message[:limit_of_length])
    verdict = analyzer.polarity_scores(translated_message)

    return Verdict(
            positive=verdict.get("pos"),
            neutral=verdict.get("neu"),
            negative=verdict.get("neg")
    )
