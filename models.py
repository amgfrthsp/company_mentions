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
    verdict: typing.Any
