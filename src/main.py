from logging import getLogger, Logger

from logging_config.setup_logger import setup_logger
from scrapers.cli import get_args
from scrapers.scraper import setup_scraper
from scrapers.country_scraper import check_country_is_supported
from scrapers.country_scraper import CountryNotSupportedError


def main():
    setup_logger()
    logger: Logger = getLogger()
    args: dict[str, str] = get_args()  # TODO: Add error handling
    check_country_is_supported(args['country'])
    print('Passed')




if __name__ == '__main__':
    main()