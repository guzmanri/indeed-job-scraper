import argparse
from argparse import ArgumentParser
from logging import getLogger, Logger

from dataclasses import dataclass

logger: Logger = getLogger()

@dataclass
class JobArgs:
    job_title: str
    country: str
    city: str
    max_pages: int

def get_args() -> JobArgs:
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

    args: argparse.Namespace = parser.parse_args()

    try:
        max_pages = int(args.max_pages)  # Truncates decimal automatically
        if max_pages < 1:
            raise ValueError
    except ValueError as e:
        error_message: str = f'--max-pages must be a positive integer: {e}'
        logger.warning(error_message)
        raise ValueError(error_message)

    return JobArgs(
        job_title=args.job_title,
        country=args.country,
        city=args.city,
        max_pages=max_pages
    )