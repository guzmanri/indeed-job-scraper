from logging import Logger, getLogger
import time
from typing import Any

import pyautogui
import pyperclip

logger: Logger = getLogger()

def timed(func):
    def wrapper(*args, **kwargs):
        start: float = time.time()
        result: Any = func(*args, **kwargs)  # Type depends on func
        end: float = time.time()
        logger.info(f'{func.__name__} took {end-start:.2f} seconds')
        return result
    return wrapper

@timed
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

@timed  # TODO: Refactor
def copy_paste() -> str:
    raw_html: str = ' Cloudflare Pages Analytics '
    while ' Cloudflare Pages Analytics ' in raw_html:
        pyautogui.hotkey('command', 'u')

        time.sleep(1)

        pyautogui.hotkey('command', 'a')
        pyautogui.hotkey('command', 'c')
        raw_html = str(pyperclip.paste())

        if ' Cloudflare Pages Analytics ' in raw_html:
            print('cloudflare blocked')
            pyautogui.hotkey('command', 'w')
            pyautogui.moveTo(500, 200)
            pyautogui.click()
            time.sleep(2)

    return raw_html

@timed
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
