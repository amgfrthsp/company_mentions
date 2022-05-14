from content_extractor import meduza_getter
import db


def get_content(companies):
    mention_dicts = []
    mention_dicts.extend(meduza_getter.get_meduza_mentions_for_companies(companies))
    mentions = []
    # Vk, Google Play, ...
    for mention_dict in mention_dicts:
        mentions.extend(db.Mention(
            mention_dict["company_id"],
            mention_dict["url"],
            mention_dict["title"],
            mention_dict["timestamp"],
            mention_dict["content"],
            mention_dict["mention_type"]
        ))
    return mentions


def get_mentions_for_companies(companies):
    mentions = get_content(companies)
