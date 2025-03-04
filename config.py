import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'your_username'),
    'password': os.getenv('MYSQL_PASSWORD', 'your_password'),
    'database': os.getenv('MYSQL_DB', 'your_database'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}