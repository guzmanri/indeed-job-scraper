from logging import Logger, getLogger
import time
from typing import Any

import pyautogui
import pyperclip

from bs4 import BeautifulSoup, ResultSet, Tag

logger: Logger = getLogger()

def timer(func):
    def wrapper(*args, **kwargs):
        start: float = time.time()
        result: Any = func(*args, **kwargs)  # Type depends on func
        end: float = time.time()
        logger.info(f'{func.__name__} took {end-start:.2f} seconds')
        return result
    return wrapper

@timer
def setup_scraper() -> None:
    """
    Assert FireFox is already running.
    :return:
    """
    pyautogui.keyDown('command')
    pyautogui.press('space')
    pyautogui.keyUp('command')
    pyautogui.write('firefox')
    pyautogui.press('enter')
    pyautogui.hotkey('command', 'shift', 'p')

    time.sleep(1)

    pyautogui.hotkey('command', 'shift', 'f')

    time.sleep(1)

def copy_paste() -> str:
    raw_html: str = ' Cloudflare Pages Analytics '
    while ' Cloudflare Pages Analytics ' in raw_html:
        pyautogui.hotkey('command', 'u')

        time.sleep(1)

        pyautogui.hotkey('command', 'a')
        pyautogui.hotkey('command', 'c')
        raw_html: str = str(pyperclip.paste())

        if ' Cloudflare Pages Analytics ' in raw_html:
            print('cloudflare blocked')
            pyautogui.hotkey('command', 'w')
            pyautogui.moveTo(500, 200)
            pyautogui.click()
            time.sleep(2)

    return raw_html

@timer
def scrape_html(url: str) -> str:
    """
    Assert FireFox browser is opened and focused.
    :param url:
    :return:
    """
    pyautogui.hotkey('command', 't')
    pyperclip.copy(url)
    pyautogui.hotkey('command', 'v')
    pyautogui.hotkey('enter')

    time.sleep(1)

    raw_html: str = copy_paste()

    for _ in range(2):
        pyautogui.hotkey('command', 'w')

    return raw_html



def extract_country_elements(html_soup: BeautifulSoup) -> ResultSet:
    return html_soup.find_all('li', class_='worldwide__country')

def extract_country_info(country_element: Tag) -> tuple[str, str]:
    country_name: str = country_element.find('span', class_='worldwide__name').text
    country_code: str = country_element.find('a')['data-country-code']
    return country_name, country_code

def get_supported_regions() -> dict[tuple[str, str], str]:
    setup_scraper()
    raw_html: str = scrape_html('https://www.indeed.com/worldwide')
    html_soup: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    country_elements: ResultSet = extract_country_elements(html_soup)

    supported_regions: dict[tuple[str, str], str] = {}
    for country_element in country_elements:
        country_info: tuple[str, str] = extract_country_info(country_element)
        supported_regions[country_info] = country_info[1]

    return supported_regions
