import json
from logging import getLogger, Logger

from bs4 import BeautifulSoup, ResultSet, Tag

from scraper import setup_scraper, scrape_html

logger: Logger = getLogger()

class CountryNotSupportedError(Exception):
    pass

def update_supported_countries_json() -> None:
    supported_countries: dict[tuple[str, str], str] = _scrape_supported_countries()
    serialized_data: dict[str, str] = {'|'.join(key): value for key, value in supported_countries.items()}
    with open('supported_countries.json', 'w', encoding='utf-8') as file:
        json.dump(serialized_data, file, indent=4)  # NOQA - TextIO vs SupportsWrite[str]

def _read_supported_countries_json() -> dict[tuple[str, ...], str]:
    with open('scrapers/supported_countries.json', 'r', encoding='utf-8') as file:
        loaded_data: dict[str, str] = json.load(file)
    return {tuple(key.split("|")): value for key, value in loaded_data.items()}

def _check_country_is_supported(country: str) -> None:
    supported_countries: dict[tuple[str, ...], str] = _read_supported_countries_json()
    if not any(country in key for key in supported_countries.keys()):
        error_message: str = f'Country "{country}" is not supported.'
        logger.info(error_message)
        help_message: str = 'Please choose a country or country code from the following list:'
        for supported_country in supported_countries:
            help_message += f'\n{supported_country[0]} ({supported_country[1]})'
        raise CountryNotSupportedError(f'{error_message} {help_message}')

def _extract_country_elements(html_soup: BeautifulSoup) -> ResultSet:
    return html_soup.find_all('li', class_='worldwide__country')

def _extract_country_info(country_element: Tag) -> tuple[str, str]:
    country_name: str = country_element.find('span', class_='worldwide__name').text
    country_code: str = country_element.find('a')['data-country-code']
    return country_name, country_code

def _scrape_supported_countries() -> dict[tuple[str, str], str]:
    setup_scraper()
    raw_html: str = scrape_html('https://www.indeed.com/worldwide')
    html_soup: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    country_elements: ResultSet = _extract_country_elements(html_soup)
    supported_countries: dict[tuple[str, str], str] = {}
    for country_element in country_elements:
        country_info: tuple[str, str] = _extract_country_info(country_element)
        if country_info[1] == 'us':
            supported_countries[country_info] = 'www'
        else:
            supported_countries[country_info] = country_info[1]
    return supported_countries

if __name__ == '__main__':
    update_supported_countries_json()