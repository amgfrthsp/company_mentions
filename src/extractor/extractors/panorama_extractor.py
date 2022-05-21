import calendar
import datetime

from bs4 import BeautifulSoup
import requests
import re

from models import Mention, MentionTypes

NAME = "panorama"

PANORAMA_URL = "https://panorama.pub"


def get_pubs():
    page = requests.get(PANORAMA_URL)
    soup = BeautifulSoup(page.text, "html.parser")
    raw_articles = soup.find_all('a', {'href': re.compile(r'/news/*')})
    pubs = {}
    for article in raw_articles:
        try:
            article_url = PANORAMA_URL + article['href']

            meta = article.find_all('div')
            title = meta[len(meta) - 1].contents[0].strip()

            article_page = requests.get(article_url)
            article_soup = BeautifulSoup(article_page.text, "html.parser")

            date = article_soup.find('meta', {'itemprop': 'datePublished'})['content']
            timestamp = calendar.timegm(
                datetime.datetime.strptime(date, "%Y-%m-%d").timetuple()
            )

            content_block = article_soup.find('div', {'itemprop': "articleBody"})
            paragraphs = content_block.find_all('p')
            content = ""
            for paragraph in paragraphs:
                content += paragraph.contents[0] + '\n'
            pubs[article_url] = {
                'url': article_url,
                'timestamp': timestamp,
                'title': title,
                'content': content
            }
        except Exception:
            continue
    return list(pubs.values())


def search_for_company(pubs, company_name) -> list[Mention]:
    mentions = []
    for pub in pubs:
        if re.search(company_name, pub["content"], re.IGNORECASE):
            mentions.append(Mention(company_name=company_name,
                                    url=pub["url"],
                                    title=pub["title"],
                                    timestamp=pub["timestamp"],
                                    content=pub["content"],
                                    type=MentionTypes.MEM))
    return mentions


def get_last_mentions(company_name) -> list[Mention]:
    all_pubs = get_pubs()
    mentions = search_for_company(all_pubs, company_name)
    return mentions
