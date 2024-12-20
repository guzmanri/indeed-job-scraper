from database import *
from logging_config import *

def main():
    setup_logger()
    create_database()

if __name__ == '__main__':
    main()