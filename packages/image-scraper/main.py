import os
from datetime import date
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def get_html(url: str) -> str:
    """
    Returns the HTML for a given webpage.
    """
    desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
    desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) ' \
                                                                      'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                                                      'Chrome/39.0.2171.95 Safari/537.36'
    browser = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
    browser.get(url)
    html = browser.page_source
    return html


def get_soup(url: str):
    """
    Returns object describing content downloaded from url.
    """
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_daily_search_term() -> str:
    """
    Get daily search term from SketchDaily subreddit.
    """
    soup = get_soup('https://www.reddit.com/r/SketchDaily/')
    todays_header = soup.find('h3')

    parts = todays_header.text.split('-')
    search_term = parts[1].strip()
    print(f'search term for today: {search_term}')
    return search_term


def scrape_top_100_results(search_term: str = get_daily_search_term()) -> None:
    """
    Downloads the top 100 results of images from duckduckgo.
    """
    base_url = 'https://duckduckgo.com/'
    query_params = {
        'ia': 'images',
        'iax': 'images',
        'q': search_term,
    }
    querystring = urlencode(query_params)
    images_url = f'{base_url}?{querystring}'

    soup = get_soup(images_url)
    image_items = soup.find_all('img', 'tile--img__img')

    # create directory for today's date
    date_string = str(date.today())
    todays_directory = os.path.join(
        os.path.dirname(__file__),
        'scrapes',
        date_string)
    os.makedirs(todays_directory, exist_ok=True)

    for item in image_items:
        image_source = f"https:{item['src']}"
        print(f'downloading {image_source}')
        res = requests.get(image_source)

        filename = f"scrapes/{date_string}/{item['alt']}.jpeg"
        file = open(filename, 'wb')
        file.write(res.content)
        file.close()


if __name__ == "__main__":
    scrape_top_100_results()
