import typing
from dataclasses import dataclass
from enum import Enum


class MentionTypes(Enum):
    NEWS = "news"
    POST = "post"


@dataclass
class Mention:
    company_name: str
    title: str
    content: str
    url: str
    timestamp: int
    type: MentionTypes


@dataclass
class ClassifiedMention:
    url: str
    positive: float
    neutral: float
    negative: float

