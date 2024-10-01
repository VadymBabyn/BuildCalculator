from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from controller.user_controller import UserController

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Login')

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton('Register', self)
        self.register_button.clicked.connect(self.open_register_page)

        layout = QVBoxLayout()
        layout.addWidget(QLabel('Login'))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_controller = UserController()
        user = user_controller.login(username, password)

        if user:
            self.open_home_page(user)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid username or password.')

    def open_home_page(self, user):
        from views.house_grid import HouseGridWindow
        self.home_page = HouseGridWindow(is_admin=(user.role == 'admin'))
        self.close()
        self.home_page.exec_()


    def open_register_page(self):
        from views.register import RegisterPage
        self.register_page = RegisterPage()
        self.register_page.show()
        self.close()
