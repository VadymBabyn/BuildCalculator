import sys
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from views.login import LoginPage

def main():
    app = QApplication(sys.argv)
    if getattr(sys, 'frozen', False):
        photo_path = sys._MEIPASS
    else:
        photo_path = os.path.dirname(os.path.abspath(__file__))
    photo_file_path = os.path.join(photo_path, 'photo/logo.jpg')
    app.setWindowIcon(QIcon(photo_file_path))

    try:
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        style_file_path = os.path.join(application_path, 'styles.qss')
        with open(style_file_path, "r") as file:
            app.setStyleSheet(file.read())
    except FileNotFoundError:
        print("'styles.qss' not found. Applying default styles.")
    except Exception as e:
        print(f"Error loading styles.qss: {e}")

    login_page = LoginPage()
    login_page.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
