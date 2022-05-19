from dataclasses import dataclass, field
from enum import Enum


class MentionTypes(Enum):
    NEWS = "news"
    POST = "post"
    MEM = "mem"


class SentimentTypes(Enum):
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


@dataclass
class Mention:
    company_name: str
    content: str
    url: str
    timestamp: int
    type: MentionTypes
    title: str = ""


# @dataclass
# class ClassifiedMention:
#     url: str
#     positive: float
#     neutral: float
#     negative: float


@dataclass
class Verdict:
    positive: float
    neutral: float
    negative: float


@dataclass
class NotificationContent:
    title: str
    content: str
    url: str
    sentiment: SentimentTypes


@dataclass
class CompanyNotifications:
    company_name: str
    user_ids: list[int]
    news: list[NotificationContent] = field(default_factory=list)
    posts: list[NotificationContent] = field(default_factory=list)
    mems: list[NotificationContent] = field(default_factory=list)
