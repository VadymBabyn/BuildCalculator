from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from controller.user_controller import UserController

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Register')

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.register)

        self.back_button = QPushButton('Back to Login', self)
        self.back_button.clicked.connect(self.back_to_login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Register'))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Call to service method to register user
        user_service = UserService()
        try:
            user_service.register_user(username, password)
            QMessageBox.information(self, 'Success', 'User registered successfully!')
            self.back_to_login()
        except Exception as e:
            QMessageBox.warning(self, 'Registration Failed', str(e))

    def back_to_login(self):
        from views.login import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()
