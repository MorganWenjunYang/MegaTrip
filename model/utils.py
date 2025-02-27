import mysql.connector
from config import DB_CONFIG

def connect_to_db():
    """Create and return a database connection"""
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(query, params=None, fetch=True):
    """Execute a query and optionally return results"""
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetch:
            result = cursor.fetchall()
            return result
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()