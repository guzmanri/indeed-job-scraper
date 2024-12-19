import json

from bs4 import BeautifulSoup, ResultSet, Tag

from scraper import setup_scraper, scrape_html


def extract_country_elements(html_soup: BeautifulSoup) -> ResultSet:
    return html_soup.find_all('li', class_='worldwide__country')

def extract_country_info(country_element: Tag) -> tuple[str, str]:
    country_name: str = country_element.find('span', class_='worldwide__name').text
    country_code: str = country_element.find('a')['data-country-code']
    return country_name, country_code

def scrape_supported_regions() -> dict[tuple[str, str], str]:
    setup_scraper()
    raw_html: str = scrape_html('https://www.indeed.com/worldwide')
    html_soup: BeautifulSoup = BeautifulSoup(raw_html, 'html.parser')
    country_elements: ResultSet = extract_country_elements(html_soup)

    supported_regions: dict[tuple[str, str], str] = {}
    for country_element in country_elements:
        country_info: tuple[str, str] = extract_country_info(country_element)
        if country_info[1] == 'us':
            supported_regions[country_info] = 'www'
        else:
            supported_regions[country_info] = country_info[1]

    return supported_regions

def update_supported_regions_json() -> None:
    supported_regions: dict[tuple[str, str], str] = scrape_supported_regions()
    serialized_data: dict[str, str] = {'|'.join(key): value for key, value in supported_regions.items()}
    with open('supported_regions.json', 'w', encoding='utf-8') as file:
        json.dump(serialized_data, file, indent=4)  # NOQA - TextIO vs SupportsWrite[str]

def read_supported_regions_json() -> dict[tuple[str, ...], str]:
    with open('supported_regions.json', 'r', encoding='utf-8') as file:
        loaded_data: dict[str, str] = json.load(file)
    return {tuple(key.split("|")): value for key, value in loaded_data.items()}

if __name__ == '__main__':
    update_supported_regions_json()