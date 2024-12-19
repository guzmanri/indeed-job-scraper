import argparse
from argparse import ArgumentParser

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
        help='The country code to search for (e.g., "US").'
    )

    parser.add_argument(
        '--city',
        type=str,
        default='remote',
        help='The city to search near (e.g., Toronto). Defaults to "remote".'
    )

    parser.add_argument(
        '--max-pages',
        type=str,
        default='10',
        help='The maximum number of pages to search. Defaults to "10".'
    )

    args: argparse.Namespace = parser.parse_args()
    return {arg: getattr(args, arg).title().strip() for arg in vars(args)}