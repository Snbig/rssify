import os
from urllib.parse import urljoin
from datetime import datetime
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from pytz import timezone
from hashlib import sha1

title = os.environ.get('TITLE')
subtitle = os.environ.get('SUBTITLE')
url = os.environ.get('URL')
author_name = os.environ.get('AUTHOR_NAME')
author_email = os.environ.get('AUTHOR_EMAIL')
language = os.environ.get('LANGUAGE')
item_title_selector = os.environ.get('ITEM_TITLE_CSS')
item_url_selector = os.environ.get('ITEM_URL_CSS')
item_author_selector = os.environ.get('ITEM_AUTHOR_CSS')
item_description_selector = os.environ.get('ITEM_DESCRIPTION_CSS')
item_date_selector = os.environ.get('ITEM_DATE_CSS')
item_date_format = os.environ.get('ITEM_DATE_FORMAT')
item_timezone = os.environ.get('ITEM_TIMEZONE')

r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
titles = soup.select(item_title_selector)
urls = soup.select(item_url_selector)
fg.subtitle(subtitle)

descriptions = []
if item_description_selector:
    descriptions = soup.select(item_description_selector)

authors = []
if item_author_selector:
    authors = soup.select(item_author_selector)

dates = []
if item_date_selector:
    dates = soup.select(item_date_selector)

fg = FeedGenerator()
fg.id(url)
fg.title(title)

fg.link(href='https://tabhub.github.io/', rel='alternate')
fg.language(language)
fg.author({'name': author_name, 'email': author_email})

for i in range(len(titles)):
    if i > len(urls) - 1:
        break

    fe = fg.add_entry()
    fe.guid(sha1(title[i].text + subtitle))
    fe.title(titles[i].text)
    item_url = urljoin(url, urls[i].get('href'))
    fe.id(item_url)
    fe.link(href=item_url, rel='alternate')

    if descriptions and descriptions[i]:
        fe.description(descriptions[i].text)

    if authors and authors[i]:
        fe.author(name=authors[i].text)

    if dates and item_date_format:
        date = datetime.strptime(dates[i].text.strip(), item_date_format)
    else:
        date = datetime.utcnow()

    localtz = timezone(item_timezone)
    date = localtz.localize(date)
    fe.published(date)
    fe.updated(date)

fg.atom_file('atom.xml')
