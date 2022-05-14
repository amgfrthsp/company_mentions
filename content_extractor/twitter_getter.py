import logging
import json
import requests
from decouple import config


def create_url(query):
    tweet_fields = 'id,text,created_at'
    url = f'https://api.twitter.com/2/tweets/search/recent?query={query}&tweet.fields={tweet_fields}'
    return url


def create_news_url(company_name):
    query = f'"{company_name}" (lang:en OR lang:ru) is:verified -is:retweet -is:reply -is:quote has:links'
    return create_url(query)


def create_social_medias_url(company_name):
    query = f'{company_name} (lang:en OR lang:ru) is:verified -is:retweet -is:reply -is:quote -has:links'
    return create_url(query)


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    logging.info(response.status_code)
    if response.status_code != 200:
        raise Exception(f'Request returned an error: {response.status_code} {response.text}')
    return response.json()


if __name__ == "__main__":
    BEARER_TOKEN = config('TWITTER_BEARER_TOKEN')
    url = create_social_medias_url('Coca-cola')
    json_response = connect_to_endpoint(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))