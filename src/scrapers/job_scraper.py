from bs4 import BeautifulSoup, ResultSet, Tag

from scraper import scrape_html, timed

@timed
def scrape_job_pages(num_pages: int, base_url: str) -> dict[int, str]:
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