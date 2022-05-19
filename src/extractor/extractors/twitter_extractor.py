import logging
import json
import requests
from decouple import config
from models import Mention, MentionTypes


def create_url(query: str) -> str:
    tweet_fields = 'id,text,created_at'
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields={tweet_fields}&max_results=100'
    return url


def create_news_url(company_name: str) -> str:
    query = f'(("{company_name}") (lang:en OR lang:ru) is:verified -is:retweet -is:reply -is:quote has:links)'
    return create_url(query)


def create_social_medias_url(company_name: str) -> str:
    query = f'({company_name} OR from:"{company_name}") (lang:en OR lang:ru) is:verified -is:retweet -is:reply -is:quote -has:links'
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
    response = requests.request("GET", url, auth=bearer_oauth)
    #logging.info(response.status_code)
    if response.status_code != 200:
        raise Exception(f'Request returned an error: {response.status_code} {response.text}')
    return response.json()


def get_last_mentions(company_name) -> list[Mention]:
    mentions = []

    url = create_news_url(company_name)
    json_response = connect_to_endpoint(url)
    if json_response["meta"]["result_count"] != 0:
        for tweet in json_response["data"]:
            mentions.append(Mention(
                company_name=company_name,
                content=tweet["text"],
                url=f'https://twitter.com/anyuser/status/{tweet["id"]}',
                timestamp=tweet["created_at"],
                type=MentionTypes.NEWS
            ))

    url = create_social_medias_url(company_name)
    json_response = connect_to_endpoint(url)
    if json_response["meta"]["result_count"] != 0:
        for tweet in json_response["data"]:
            mentions.append(Mention(
                company_name=company_name,
                content=tweet["text"],
                url=f'https://twitter.com/anyuser/status/{tweet["id"]}',
                timestamp=tweet["created_at"],
                type=MentionTypes.POST
            ))
    return mentions


if __name__ == "__main__":
    BEARER_TOKEN = config('TWITTER_BEARER_TOKEN')
    url = create_social_medias_url('Яндекс')
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))
