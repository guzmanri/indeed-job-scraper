from databases.temp_db import insert_temp_job_data
from logging_config.cli import get_args
from logging_config.setup_logger import setup_logger
def main():
    setup_logger()
    args = get_args()


if __name__ == '__main__':
    main()