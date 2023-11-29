import os
from urllib.parse import urljoin
from datetime import datetime
import requests
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
from pytz import timezone

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
titles = soup.select(item_title_selector)
urls = soup.select(item_url_selector)

desriptions = []
if item_description_selector:
    descriptions = soup.select(item_description_selector)

authors = []
if item_author_selector:
    authors = soup.select(item_author_selector)

dates = []
if item_date_selector:
    dates = soup.select(item_date_selector)

versions = []
if version_css:
    versions = soup.select(version_css)

ausers = []
if ausers_css:
    ausers = soup.select(ausers_css)
print(ausers)

ldates = []
if ldate_css:
    ldates = soup.select(ldate_css)

asizes = []
if asize_css:
    asizes = soup.select(asize_css)

fg = FeedGenerator()
fg.id(url)
fg.title(title)

fg.link(href=url, rel='via')
fg.language(language)
fg.author({'name': author_name, 'email': author_email})

for i in range(len(titles)):
    if i > len(urls) - 1:
        break

    fe = fg.add_entry()
    fe.title(titles[i].text)
    item_url = urljoin(url, urls[i].get('href'))
    if versions and versions[i]:
        fe.id(item_url + "@" + versions[i].text.strip())
    else:
         fe.id(item_url)

    fe.link(href=item_url, rel='alternate')

    if descriptions and descriptions[i]:
        custom_decs = ""
        custom_decs += f"{versions[i].text.strip()} \n" 
        custom_decs += f"{ausers[i].text.strip()} نصب فعال\n"
        custom_decs += f"{asizes[i].text.strip()} حجم \n" 
        custom_decs += f"تاریخ آخرین  به‌روزرسانی {ldates[i].text.strip()} \n" 

        fe.description(custom_decs)

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

fg.atom_file(f'{target}.xml')
