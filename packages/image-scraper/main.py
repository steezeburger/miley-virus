import requests
from datetime import date
from urllib.parse import urlencode

from bs4 import BeautifulSoup
from selenium import webdriver

def get_daily_search_term():
    return 'double rainbow'

def get_html(url):
    browser = webdriver.PhantomJS()
    browser.get(url)
    html = browser.page_source
    return html

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

    html_data = get_html(images_url)
    soup = BeautifulSoup(html_data, 'html.parser')

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
