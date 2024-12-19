import time

import pyautogui
import pyperclip

from bs4 import BeautifulSoup, ResultSet, Tag


def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'{func.__name__} took {end-start:.2f} seconds')
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

@timer
def scrape_pages(num_pages: int, base_url: str) -> dict[int, str]:
    pages_html: dict[int, str] = {}
    for start in range(0, num_pages * 10, 10):
        pages_html[1 + int(start / 10)] = scrape_html(f'{base_url}&start={start}')

    return pages_html

def extract_job_elements(html_soup: BeautifulSoup) -> ResultSet:
    return html_soup.find_all('a', class_='jcs-JobTitle css-1baag51 eu4oa1w0')

def extract_job_info(job_element: Tag) -> tuple[str, str, str]:
    job_id: str = job_element.get('id')
    job_name: str = job_element.get('aria-label').replace('full details of ', '')
    job_link: str = f'https://ca.indeed.com{job_element.get('href')}'

    return job_id, job_name, job_link