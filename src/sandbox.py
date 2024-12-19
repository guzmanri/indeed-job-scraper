from src.scraper import *

from src.utils.setup_logger import *
from src.databases.temp_db import insert_temp_job_data
setup_logger()

base_url: str = 'https://ca.indeed.com/jobs?q=Software Engineer&l=Toronto'
setup_scraper()
pages_html: dict[int, str] = scrape_pages(2, base_url)


for page_number in pages_html:
    html_soup = BeautifulSoup(pages_html[page_number], 'html.parser')
    job_elements = extract_job_elements(html_soup)
    for job_element in job_elements:
        unique_id, job_title, url = extract_job_info(job_element)
        insert_temp_job_data(unique_id, job_title, page_number, url)
