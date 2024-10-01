from db import get_connection
from repository.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def authenticate_user(self, username, password):
        user = self.user_repo.get_user_by_username(username)
        if user and user.password == password:
            return user
        else:
            return None

    def register_user(self, username, password):
        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            raise Exception("Username already exists.")
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, 'user'))
        connection.commit()
        cursor.close()
        connection.close()