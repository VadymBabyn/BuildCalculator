import sys
from PyQt5.QtWidgets import QApplication
from views.login import LoginPage

def main():
    app = QApplication(sys.argv)

    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

    login_page = LoginPage()
    login_page.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
