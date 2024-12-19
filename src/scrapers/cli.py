import argparse
from argparse import ArgumentParser
from logging import getLogger, Logger
from typing import Union

from country_scraper import _check_country_is_supported

logger: Logger = getLogger()

def get_args() -> dict[str, str]:
    parser: ArgumentParser = argparse.ArgumentParser()

    parser.add_argument(
        '--job-title',
        type=str,
        required=True,
        help='The job title to search for (e.g., "Machine Learning Engineer").'
    )

    parser.add_argument(
        '--country',
        type=str,
        required=True,
        help='The country code to search for (e.g., "United States" or "US").'
    )

    parser.add_argument(
        '--city',
        type=str,
        default='Remote',
        help='The city to search near (e.g., Toronto). Defaults to "Remote".'
    )

    parser.add_argument(
        '--max-pages',
        type=str,
        default='10',
        help='The maximum number of pages to search. Defaults to "10".'
    )

    raw_args: argparse.Namespace = parser.parse_args()
    args: dict[str, Union[str, int]] = {arg: getattr(raw_args, arg).title().strip() for arg in vars(raw_args)}
    _verify_args(args)
    return args

def _check_max_pages_is_valid(max_pages: str) -> None:
    if not max_pages.isdigit() or '-' in max_pages:
        error_message = f'Invalid max-pages: {max_pages}. Max-pages must be a positive integer.'
        logger.info(error_message)
        raise ValueError(error_message)

def _verify_args(args: dict[str, Union[str, int]]) -> None:
    _check_country_is_supported(args['country'])
    _check_max_pages_is_valid(args['max_pages'])
    args['max_pages'] = int(args['max_pages'])
