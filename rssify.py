import os
from urllib.parse import urljoin
from datetime import datetime
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from pytz import timezone
import json

title = os.environ.get('TITLE')
subtitle = os.environ.get('SUBTITLE')
url = os.environ.get('URL')
target = os.environ.get('TARGET')
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
version_css = os.environ.get('VERSION_CSS')
ausers_css = os.environ.get('AUSERS_CSS')
ldate_css = os.environ.get('LDATE_CSS')
asize_css = os.environ.get('ASIZE_CSS')


r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

titles = soup.select_one(item_title_selector)
urls = soup.select_one(item_url_selector)

if target== 'charkhoneh':
    char = json.dumps(titles.text, indent=2)
    print(json.loads(char)['@graph'][2]['softwareVersion'])

desriptions = []
if item_description_selector:
    descriptions = soup.select_one(item_description_selector)

authors = []
if item_author_selector:
    authors = soup.select_one(item_author_selector)

dates = []
if item_date_selector:
    dates = soup.select_one(item_date_selector)

versions = []
if version_css:
    versions = soup.select_one(version_css)

ausers = []
if ausers_css:
    ausers = soup.select_one(ausers_css)

ldates = []
if ldate_css:
    ldates = soup.select_one(ldate_css)

asizes = []
if asize_css:
    asizes = soup.select_one(asize_css)

fg = FeedGenerator()
fg.id(url)
fg.title(title)

fg.link(href=url, rel='via')
fg.language(language)
fg.author({'name': author_name, 'email': author_email})

fe = fg.add_entry()
fe.title(titles.text)
item_url = urljoin(url, urls.get('href'))

if target == 'anardoni':
    versions = json.loads(versions.text)['softwareVersion']
    fe.id(item_url + "@" + versions)
else:
    fe.id(item_url + "@" + versions.text.strip())

fe.link(href=item_url, rel='alternate')

if descriptions and descriptions:
    custom_decs = ""
    custom_decs += f"{versions if target == 'anardoni' else versions.text.strip()} \n" 
    custom_decs += f"{ausers.text.strip()} نصب فعال\n"
    custom_decs += f"{asizes.text.strip()} حجم \n" 
    custom_decs += f"تاریخ آخرین  به‌روزرسانی {ldates.text.strip()} \n" 

    fe.description(custom_decs)

if authors and authors:
    fe.author(name=authors.text)

if dates and item_date_format:
    date = datetime.strptime(dates.text.strip(), item_date_format)
else:
    date = datetime.utcnow()

localtz = timezone(item_timezone)
date = localtz.localize(date)
fe.published(date)
fe.updated(date)

fg.atom_file(f'./feeds/{target}.xml')
