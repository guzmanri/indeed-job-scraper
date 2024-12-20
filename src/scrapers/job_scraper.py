from bs4 import BeautifulSoup, ResultSet, Tag
from dataclasses import dataclass

from .cli import JobArgs
from .country_scraper import _get_country_code
from .scraper import _scrape_html, _setup_scraper, _timed

@dataclass
class Job:
    unique_id: str
    job_title: str
    page_number: int
    url: str
    company_name: str = None
    salary: str = None
    job_type: str = None
    location: str = None
    benefits: str = None
    job_description: str = None
    is_fully_processed: bool = False

def get_base_url(args: JobArgs) -> str:
    return f'https://{_get_country_code(args.country)}.indeed.com/jobs?q={args.job_title}&l={args.city}'

@_timed
def scrape_job_pages(num_pages: int, base_url: str) -> list[Job]:
    _setup_scraper()

    pages_html: dict[int, str] = {}
    for start in range(0, num_pages * 10, 10):
        pages_html[1 + int(start / 10)] = _scrape_html(f'{base_url}&start={start}')

    jobs_basic_info: list[Job] = []
    for page_number in pages_html:
        html_soup: BeautifulSoup = BeautifulSoup(pages_html[page_number], 'html.parser')
        job_elements: ResultSet = _extract_job_elements(html_soup)

        for job_element in job_elements:
            unique_id, job_title, url = _extract_basic_job_info(job_element)
            jobs_basic_info.append(Job(unique_id, job_title, page_number, url))

    return jobs_basic_info

def _extract_job_elements(html_soup: BeautifulSoup) -> ResultSet:
    return html_soup.find_all('a', class_='jcs-JobTitle css-1baag51 eu4oa1w0')

def _extract_basic_job_info(job_element: Tag) -> tuple[str, str, str]:
    unique_id: str = job_element.get('id')
    job_title: str = job_element.get('aria-label').replace('full details of ', '')
    url: str = f'https://ca.indeed.com{job_element.get('href')}'

    return unique_id, job_title, url
