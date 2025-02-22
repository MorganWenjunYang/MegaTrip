import mysql.connector
import utils

class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email

    def save_to_db(self):
        db = self.connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (user_id, name, email) VALUES (%s, %s, %s)", (self.user_id, self.name, self.email))
        db.commit()
        cursor.close()
        db.close()

    @staticmethod
    def get_user(user_id):
        db = utils.connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        db.close()
        if user_data:
            return User(*user_data)
        return None