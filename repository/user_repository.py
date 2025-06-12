from db import get_connection
from models.user import User

class UserRepository:
    def get_user_by_username(self, username):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        row = cursor.fetchone()
        if row:
            user = User(row[0], row[1], row[2], row[3])
        else:
            user = None
        cursor.close()
        connection.close()
        return user

    def add_user(self, username, hashed_password, role='user'):
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role)
        )
        connection.commit()
        cursor.close()
        connection.close()
