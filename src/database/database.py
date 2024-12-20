import logging
import os

from dotenv import load_dotenv
import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

from ..scrapers import Job

load_dotenv()
logger = logging.getLogger()

class DatabaseConnectionError(Exception):
    pass

class DatabaseInsertionError(Exception):
    pass

def create_database() -> None:
    try:
        connection: MySQLConnectionAbstract = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
        )
    except mysql.connector.Error as e:
        error_message: str = f'Unable to fetch database info from .env: {e}'
        logger.error(error_message)
        raise DatabaseConnectionError(error_message)

    cursor: MySQLCursorAbstract = connection.cursor()

    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}')
    cursor.execute(f'USE {os.getenv('DB_NAME')}')
    logger.info(f'Database {os.getenv('DB_NAME')} created successfully.')

    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {os.getenv('DB_TABLE')} (
        unique_id VARCHAR(255) PRIMARY KEY,
        job_title VARCHAR(255) NOT NULL,
        page_number INT NOT NULL,
        scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        url TEXT NOT NULL,
        company_name VARCHAR(255) DEFAULT NULL,
        salary VARCHAR(255) DEFAULT NULL,
        job_type varchar(255) DEFAULT NULL,
        location VARCHAR(255) DEFAULT NULL,
        benefits TEXT DEFAULT NULL,
        job_description TEXT DEFAULT NULL,
        is_fully_processed BOOLEAN DEFAULT FALSE
    );
    ''')

    cursor.close()
    connection.close()

    logger.info(f'Table {os.getenv('DB_TABLE')} created successfully.')
    return

def insert_job_data(job: Job) -> None:
    connection: MySQLConnectionAbstract = _connect_to_database()
    cursor: MySQLCursorAbstract = connection.cursor()
    try:
        cursor.execute('''
            INSERT IGNORE INTO jobs_data (
            unique_id,
            job_title,
            page_number,
            url,
            company_name,
            salary,
            job_type,
            location,
            benefits,
            job_description,
            is_fully_processed)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (
                job.unique_id,
                job.job_title,
                job.page_number,
                job.url,
                job.company_name,
                job.salary,
                job.job_type,
                job.location,
                job.benefits,
                job.job_description,
                job.is_fully_processed
            )
        )
        connection.commit()
    except mysql.connector.Error as e:
        error_message: str = f'Failed to insert data into temporary database: {e}'
        logger.error(error_message)
        raise DatabaseInsertionError(error_message)

    cursor.close()
    connection.close()

    logger.info(f'Successfully inserted data into temporary database: {job.unique_id}')
    return

def _connect_to_database() -> MySQLConnectionAbstract:
    try:
        connection: MySQLConnectionAbstract = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT'),
        )
    except mysql.connector.Error as e:
        error_message: str = f'Failed to connect to database: {e}'
        logger.error(error_message)
        raise DatabaseConnectionError(error_message)

    logger.info('Successfully connected to database.')
    return connection
