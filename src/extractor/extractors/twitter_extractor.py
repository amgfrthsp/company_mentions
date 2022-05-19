import logging
import datetime
import time
import requests
from decouple import config
from models import Mention, MentionTypes

NAME = "twitter"


def create_url(query: str) -> str:
    tweet_fields = 'id,text,created_at'
    max_results = 10
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields={tweet_fields}&max_results={max_results}'
    return url


def create_news_url(company_name: str) -> str:
    query = f'("{company_name}" (lang:en OR lang:ru) is:verified -is:retweet -is:reply -is:quote has:links)'
    return create_url(query)


def create_posts_url(company_name: str) -> str:
    query = f'(({company_name} OR from:"{company_name}") (lang:en OR lang:ru) is:verified -is:retweet -is:reply ' \
            f'-is:quote -has:links)'
    return create_url(query)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    BEARER_TOKEN = config('TWITTER_BEARER_TOKEN')
    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.get(url, auth=bearer_oauth)
    logging.info(response.status_code)
    if response.status_code != 200:
        raise Exception(f'Request returned an error: {response.status_code} {response.text}')
    return response.json()


def add_mentions_from_tweets(company_name: str, mentions: list[Mention], tweets: list[dict], type: MentionTypes):
    for tweet in tweets:
        timestamp = time.mktime(datetime.datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())
        mentions.append(Mention(
            company_name=company_name,
            content=tweet["text"],
            url=f'https://twitter.com/anyuser/status/{tweet["id"]}',
            timestamp=int(timestamp),
            type=type
        ))


def get_last_mentions(company_name: str) -> list[Mention]:
    mentions = []

    json_response = connect_to_endpoint(create_news_url(company_name))
    if json_response["meta"]["result_count"]:
        add_mentions_from_tweets(company_name, mentions, json_response["data"], MentionTypes.NEWS)

    json_response = connect_to_endpoint(create_posts_url(company_name))
    if json_response["meta"]["result_count"]:
        add_mentions_from_tweets(company_name, mentions, json_response["data"], MentionTypes.POST)

    return mentions


if __name__ == "__main__":
    company = 'Bershka'
    print(get_last_mentions(company))
