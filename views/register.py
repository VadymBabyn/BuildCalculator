from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt
from service.user_service import UserService

class RegisterPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Реєстрація')
        self.setFixedSize(400, 280)

        # Заголовок
        self.title_label = QLabel('Реєстрація')
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
        self.register_button = QPushButton('Зареєструватися', self)
        self.register_button.setStyleSheet("""
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
        self.register_button.clicked.connect(self.register)

        self.back_button = QPushButton('Назад до входу', self)
        self.back_button.setStyleSheet("""
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
        self.back_button.clicked.connect(self.back_to_login)

        # Розмітка
        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()

        user_service = UserService()
        try:
            user_service.register_user(username, password)
            QMessageBox.information(self, 'Успішно', 'Користувача зареєстровано успішно!')
            self.back_to_login()
        except Exception as e:
            QMessageBox.warning(self, 'Помилка реєстрації', str(e))

    def back_to_login(self):
        from views.login import LoginPage
        self.login_page = LoginPage()
        self.login_page.show()
        self.close()
