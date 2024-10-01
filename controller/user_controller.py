from service.user_service import UserService

class UserController:
    def __init__(self):
        self.user_service = UserService()

    def login(self, username, password):
        return self.user_service.authenticate_user(username, password)
