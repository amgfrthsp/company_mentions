from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

from models import ClassifiedMention

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def classify(mentions):
    messages = [mention.content for mention in mentions]
    verdicts = model.predict(messages, k=2)

    classified_mentions = []

    for i in range(0, len(messages)):
        classified_mentions.append(ClassifiedMention(
            id=0,
            base_mention_id=mentions[i].id,
            positive=verdicts[i].get("positive"),
            neutral=verdicts[i].get("neutral"),
            negative=verdicts[i].get("negative")))
    return classified_mentions
