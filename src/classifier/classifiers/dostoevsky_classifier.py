from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

from models import Verdict

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def classify(message) -> Verdict:
    verdict = model.predict([message], k=2)[0]

    return Verdict(
        positive=verdict.get("positive"),
        neutral=verdict.get("neutral"),
        negative=verdict.get("negative")
    )

# def classify(mentions):
#     messages = [mention.content for mention in mentions]
#     verdicts = model.predict(messages, k=2)
#
#     classified_mentions = []
#
#     for i, verdict in enumerate(verdicts):
#         classified_mentions.append(ClassifiedMention(
#             url=mentions[i].url,
#             positive=verdict.get("positive"),
#             neutral=verdict.get("neutral"),
#             negative=verdict.get("negative")))
#     return classified_mentions
