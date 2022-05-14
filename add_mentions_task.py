from content_extractor import meduza_getter
import db


def get_content(companies):
    mention_dicts = []
    mention_dicts.extend(meduza_getter.get_meduza_mentions_for_companies(companies))
    # Vk, Google Play, ...
    return mention_dicts


async def add_mentions_for_companies(companies):
    mention_dicts = get_content(companies)
    for mention_dict in mention_dicts:
        mention = db.Mention(
            company_id=mention_dict["company_id"],
            url=mention_dict["url"],
            title=mention_dict["title"],
            timestamp=mention_dict["timestamp"],
            content=mention_dict["content"],
            type=mention_dict["type"],
            verdict=None,
            is_sent=False
        )