import logging
import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector.abstracts import MySQLCursorAbstract, MySQLConnectionAbstract

load_dotenv()
logger = logging.getLogger()

class DatabaseInsertionError(Exception):
    pass

def connect_to_temp_db() -> MySQLConnectionAbstract:
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('TEMP_DB_NAME'),
        port=os.getenv('DB_PORT'),
    )
    
def insert_temp_job_data(unique_id: str, job_title: str, page_number: int, url: str) -> None:
    conn: MySQLConnectionAbstract = connect_to_temp_db()
    cursor: MySQLCursorAbstract = conn.cursor()
    try:
        cursor.execute('''
            INSERT IGNORE INTO temp_jobs (unique_id, job_title, page_number, url) VALUES (%s, %s, %s, %s)''',
            (unique_id, job_title, page_number, url)
        )
        conn.commit()
    except mysql.connector.Error as e:
        error_message: str = 'Failed to insert data into temporary database'
        logger.error(f'{error_message}: {e}')
    logger.info(f'Successfully inserted data into temporary database: {unique_id}')
