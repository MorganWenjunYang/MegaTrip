import os
from dotenv import load_dotenv

# Load .env file only if it exists (i.e., when running locally)
if os.path.exists('.env'):
    load_dotenv()

# otherwise, use the environment variables defined in the Dockerfile/Compose file

DB_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'your_username'),
    'password': os.getenv('MYSQL_PASSWORD', 'your_password'),
    'database': os.getenv('MYSQL_DB', 'your_database'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}