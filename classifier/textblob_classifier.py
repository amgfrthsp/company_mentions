import translators as ts
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

from models import ClassifiedMention

limit_of_length = 5000 - 5


def classify(mentions):
    messages = [ts.google(mention.content[:limit_of_length]) for mention in mentions]
    verdicts = [TextBlob(message, analyzer=NaiveBayesAnalyzer()).sentiment for message in messages]

    classified_mentions = []

    for i, verdict in enumerate(verdicts):
        print(verdict)
        classified_mentions.append(ClassifiedMention(
            url=mentions[i].url,
            positive=verdict.p_pos,
            neutral=0,
            negative=verdict.p_neg))
    return classified_mentions


if __name__ == '__main__':
    # import nltk
    # nltk.download('movie_reviews')
    # nltk.download('punkt')
    print(TextBlob(ts.google('Хуаю очень плохая компания'), analyzer=NaiveBayesAnalyzer()).sentiment.p_pos)