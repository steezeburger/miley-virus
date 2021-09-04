import requests
from datetime import date
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from selenium import webdriver


def get_html(url) -> str:
    """
    Returns the HTML for a given webpage.
    """
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    return html

def get_soup(url):
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

    for item in image_items:
        image_source = f"https:{item['src']}"
        res = requests.get(image_source)

        date_string = str(date.today())
        filename = f"{date_string}/scrapes/{item['alt']}"
        file = open(filename, 'wb')
        file.write(res.content)
        file.close()


if __name__ == "__main__":
    scrape_top_100_results()
