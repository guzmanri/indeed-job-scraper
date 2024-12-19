from logging_config.setup_logger import setup_logger
from scrapers.cli import get_args
from src.scrapers.scraper import setup_scraper


def main():
    setup_logger()
    args: dict[str, str] = get_args()  # Add error handling
    setup_scraper()




if __name__ == '__main__':
    main()