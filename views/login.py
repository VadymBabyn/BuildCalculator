from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from controller.user_controller import UserController

class LoginPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Вхід')
        self.setFixedSize(400, 250)

        # Заголовок

        self.title_label = QLabel('Build Calculator')
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("""
            font-family: 'Verdana';
            font-size: 24px;
            font-weight: bold;
            color: #3f51b5;
            margin-bottom: 20px;
        """)

        # Поля вводу
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Логін')
        self.username_input.setStyleSheet('padding: 8px; border-radius: 4px; border: 1px solid #dcdcdc;')

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet('padding: 8px; border-radius: 4px; border: 1px solid #dcdcdc;')

        # Кнопки
        self.login_button = QPushButton('Увійти', self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px; 
                padding: 8px; 
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
        """)
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton('Реєстрація', self)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #3f51b5; 
                color: white; 
                font-weight: bold; 
                border-radius: 5px; 
                padding: 8px; 
                border: none;
            }
            QPushButton:hover {
                background-color: #3949ab;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            QPushButton:pressed {
                background-color: #303f9f;
            }
        """)
        self.register_button.clicked.connect(self.open_register_page)

        # Розташування елементів
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)

        layout.addLayout(button_layout)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_controller = UserController()
        user = user_controller.login(username, password)

        if user:
            self.open_home_page(user)
        else:
            QMessageBox.warning(self, 'Login Failed', 'Неправильний логін або пароль.')

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
