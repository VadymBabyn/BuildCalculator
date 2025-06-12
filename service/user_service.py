from db import get_connection
from repository.user_repository import UserRepository
from utils.password_utils import hash_password, check_password
class UserService:
    def __init__(self):
        self.user_repo = UserRepository()

    def authenticate_user(self, username, password):
        user = self.user_repo.get_user_by_username(username)
        if user and check_password(password, user.password):
            return user
        return None

    def register_user(self, username, password):
        existing_user = self.user_repo.get_user_by_username(username)
        if existing_user:
            raise Exception("Username already exists.")
        hashed_pw = hash_password(password)
        self.user_repo.add_user(username, hashed_pw, role='user')