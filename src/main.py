from database import *
from logging_config import *
from scrapers import *


def main():
    setup_logger()

    args: JobArgs = get_args()
    base_url: str = get_base_url(args)

    jobs_basic_info: list[Job] = scrape_job_pages(args.max_pages, base_url)
    for job in jobs_basic_info:
        insert_job_data(
            job.unique_id,
            job.job_title,
            job.page_number,
            job.url
        )

if __name__ == '__main__':
    main()