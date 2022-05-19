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
