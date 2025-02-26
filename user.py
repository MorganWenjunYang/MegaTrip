import mysql.connector
import utils

class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def save_to_db(self):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (user_id, name, email) VALUES (%s, %s, %s)", (self.user_id, self.name, self.email))
        db.commit()
        cursor.close()
        db.close()
