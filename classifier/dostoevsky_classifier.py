from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

tokenizer = RegexTokenizer()
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def classifyMentions(mentions):
    messages = [mention["content"] for mention in mentions]
    classified = model.predict(messages, k=2)

    for i in range(0, len(messages)):
        mentions[i].update({"verdict": {"negative": classified[i].get("negative"),
                                        "positive": classified[i].get("positive"),
                                        "neutral": classified[i].get("neutral")}
                            })
    return mentions
