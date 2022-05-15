import typing
from dataclasses import dataclass
from enum import Enum


class MentionTypes(Enum):
    NEWS = "news"
    POST = "post"


@dataclass
class Mention:
    id: int
    company_name: str
    title: str
    content: str
    url: str
    timestamp: int
    type: MentionTypes


@dataclass
class ClassifiedMention:
    id: int
    base_mention_id: int
    positive: float
    neutral: float
    negative: float

