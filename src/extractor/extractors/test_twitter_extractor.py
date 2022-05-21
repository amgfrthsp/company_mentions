import unittest
from unittest import mock

from models import MentionTypes, Mention
from extractor.extractors.twitter_extractor import create_url, create_news_url, create_posts_url, add_mentions_from_tweets, \
    get_last_mentions, connect_to_endpoint

FANCY_NEWS_URL = 'https://api.twitter.com/2/tweets/search/recent?query=("fancy" (lang:en OR lang:ru) is:verified ' \
                 '-is:retweet -is:reply -is:quote has:links)&tweet.fields=id,text,created_at&max_results=10'
FANCY_NEWS_JSON = {
    'data': [{
        'created_at': '2022-05-18T13:08:09.000Z',
        'id': '1526912526134300672',
        'text': 'Fancy https://twitter.com/SofiaLadyPython/status/1455871145954226179'
    }, {
        'created_at': '2022-05-18T10:45:28.000Z',
        'id': '1526876616605171712',
        'text': '😉 fancy https://twitter.com/SofiaLadyPython/status/1472687542172540928'
    }],
    'meta': {
        'newest_id': '1526912526134300672',
        'oldest_id': '1526876616605171712',
        'result_count': 2
    }}

FANCY_POSTS_URL = 'https://api.twitter.com/2/tweets/search/recent?query=((fancy OR from:"fancy") ' \
                  '(lang:en OR lang:ru) is:verified -is:retweet -is:reply -is:quote -has:links)&tweet.fields=id,text,' \
                  'created_at&max_results=10'

FANCY_POSTS_JSON = {
    'data': [],
    'meta': {
        'result_count': 0
    }}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
        self.text = "Not found"

    def json(self):
        return self.json_data


def mocked_requests_get(*args, **kwargs):
    if args[0] == FANCY_NEWS_URL:
        return MockResponse(FANCY_NEWS_JSON, 200)
    elif args[0] == FANCY_POSTS_URL:
        return MockResponse(FANCY_POSTS_JSON, 200)

    return MockResponse(None, 404)


class TwitterExtractorCase(unittest.TestCase):
    def test_create_url(self):
        self.assertEqual(
            create_url("fancy"),
            "https://api.twitter.com/2/tweets/search/recent?query=fancy&tweet.fields=id,text,created_at&max_results=10"
        )

    def test_create_news_url(self):
        self.assertEqual(create_news_url("fancy"), FANCY_NEWS_URL)

    def test_create_posts_url(self):
        self.assertEqual(create_posts_url("fancy"), FANCY_POSTS_URL)

    def test_add_mentions_from_tweets(self):
        mentions = []
        company_name = 'MMM'
        tweets = [
            {
                'created_at': '2022-05-18T13:08:09.000Z',
                'id': '228',
                'text': 'MMM is good'
            }, {
                'created_at': '2022-05-16T13:08:09.000Z',
                'id': '239',
                'text': 'MMM is bad'
            }
        ]

        expected_mentions = [
            Mention(
                company_name=company_name,
                content="MMM is good",
                url=f'https://twitter.com/anyuser/status/228',
                timestamp=1652879289,
                type=MentionTypes.NEWS
            ),
            Mention(
                company_name=company_name,
                content="MMM is bad",
                url=f'https://twitter.com/anyuser/status/239',
                timestamp=1652706489,
                type=MentionTypes.NEWS
            )
        ]

        add_mentions_from_tweets(company_name, mentions, tweets, MentionTypes.NEWS)
        self.assertEqual(mentions, expected_mentions)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_connect_to_endpoint(self, mock_get):
        json_response = connect_to_endpoint(FANCY_NEWS_URL)
        expected_json_response = FANCY_NEWS_JSON
        self.assertEqual(json_response, expected_json_response)

        json_response = connect_to_endpoint(FANCY_POSTS_URL)
        expected_json_response = FANCY_POSTS_JSON
        self.assertEqual(json_response, expected_json_response)

        with self.assertRaises(Exception):
            connect_to_endpoint('https://random')

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_last_mentions(self, mock_get):
        company_name = "fancy"
        expected_mentions = [
            Mention(
                company_name=company_name,
                content="Fancy https://twitter.com/SofiaLadyPython/status/1455871145954226179",
                url=f'https://twitter.com/anyuser/status/1526912526134300672',
                timestamp=1652879289,
                type=MentionTypes.NEWS
            ),
            Mention(
                company_name=company_name,
                content="😉 fancy https://twitter.com/SofiaLadyPython/status/1472687542172540928",
                url=f'https://twitter.com/anyuser/status/1526876616605171712',
                timestamp=1652870728,
                type=MentionTypes.NEWS
            )
        ]

        mentions = get_last_mentions("fancy")
        self.assertEqual(mentions, expected_mentions)


if __name__ == '__main__':
    unittest.main()
