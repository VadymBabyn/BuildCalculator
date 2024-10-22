from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, QDialog
from PyQt5.QtGui import QPixmap
from controller.house_controller import HouseController
import sys

class HouseGridWindow(QDialog):
    def __init__(self, is_admin=False):
        super().__init__()
        self.setWindowTitle('Будинки')
        self.setGeometry(100, 100, 800, 600)
        self.controller = HouseController(is_admin)
        # Створюємо основне поле з сіткою
        self.grid_layout = QGridLayout()
        # Приклад будинків
        houses = self.controller.view_houses()

        # Додаємо будинки до сітки
        row, col = 0, 0
        for house in houses:
            self.add_house_block(house, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        # Якщо це адміністратор, додаємо блок для додавання нового будинку
        if is_admin:
            self.add_new_house_block(row, col)

        self.setLayout(self.grid_layout)

    def add_house_block(self, house, row, col):
        # Використовуємо ClickableHouseWidget для обробки подій наведення та кліків
        house_widget = ClickableHouseWidget(house, self)  # self тут - це HouseGridWindow

        # Додаємо контейнер до сітки
        self.grid_layout.addWidget(house_widget, row, col)

    def add_new_house_block(self, row, col):
        # Створюємо блок для додавання нового будинку (для адміністратора)
        new_house_layout = QVBoxLayout()

        # Додаємо кнопку з плюсом
        add_button = QPushButton("+", self)
        add_button.setFixedSize(150, 150)
        new_house_layout.addWidget(add_button)

        # Додаємо підпис "Додати новий будинок"
        add_label = QLabel("Додати новий будинок", self)
        new_house_layout.addWidget(add_label)

        # Додаємо поле до сітки
        self.grid_layout.addLayout(new_house_layout, row, col)

        add_button.clicked.connect(self.show_add_house_form)


    def show_add_house_form(self):
        # Вікно для введення інформації про новий будинок
        dialog = QDialog(self)
        dialog.setWindowTitle("Додати новий будинок")

        # Поля для вводу даних будинку
        layout = QVBoxLayout()

        name_input = QLineEdit(dialog)
        name_input.setPlaceholderText("Назва будинку")
        layout.addWidget(name_input)

        address_input = QLineEdit(dialog)
        address_input.setPlaceholderText("Адреса")
        layout.addWidget(address_input)

        floors_input = QLineEdit(dialog)
        floors_input.setPlaceholderText("Кількість поверхів")
        layout.addWidget(floors_input)

        # Кнопка для збереження
        save_button = QPushButton("Зберегти", dialog)
        layout.addWidget(save_button)

        save_button.clicked.connect(lambda: self.save_new_house(name_input, address_input, floors_input, dialog))

        dialog.setLayout(layout)
        dialog.exec_()


    def save_new_house(self, name_input, address_input, floors_input, dialog):
        # Отримуємо значення з полів
        name = name_input.text()
        address = address_input.text()
        floors = floors_input.text()

        # Перевіряємо, чи всі поля заповнені
        if not name or not address or not floors:
            print("Будь ласка, заповніть всі поля!")
            return

        # Зберігаємо новий будинок через контролер
        self.controller.create_house(name, address, int(floors))

        # Закриваємо форму після збереження
        dialog.accept()

        # Оновлюємо сітку будинків
        self.refresh_grid()


    def refresh_grid(self):
        # Очищаємо сітку (включно з макетами)
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item is not None:
                widget = item.widget()  # Отримуємо віджет
                if widget is not None:
                    widget.deleteLater()
                else:
                    # Якщо немає віджета, це може бути макет (layout), очищуємо його
                    layout = item.layout()
                    if layout is not None:
                        while layout.count():
                            child = layout.takeAt(0)
                            if child.widget() is not None:
                                child.widget().deleteLater()
                        self.grid_layout.removeItem(layout)
        # Додаємо будинки заново
        houses = self.controller.view_houses()
        row, col = 0, 0
        for house in houses:
            self.add_house_block(house, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        # Додаємо кнопку для нового будинку для адміністратора
        if self.controller.is_admin:
            self.add_new_house_block(row, col)


class ClickableHouseWidget(QWidget):
    def __init__(self, house, parent=None):
        super().__init__(parent)
        self.house = house
        self.setAutoFillBackground(True)
        self.init_ui()

    def init_ui(self):
        # Створюємо вертикальний layout для одного будинку
        house_layout = QVBoxLayout(self)
        house_layout.setContentsMargins(25, 0, 25, 0)  # Відступи

        # Додаємо фото будинку
        photo_label = QLabel(self)
        pixmap = QPixmap(self.house.photo)
        if not pixmap.isNull():
            photo_label.setPixmap(pixmap.scaled(150, 150, aspectRatioMode=1))
            photo_label.setScaledContents(True)
        else:
            photo_label.setText("Image not found")

        # Додаємо photo_label до layout
        house_layout.addWidget(photo_label)

        # Додаємо текстовий блок
        info_label = QLabel(f"{self.house.name}, {self.house.address}, Кількість поверхів: {self.house.floors}", self)
        info_label.setStyleSheet("background-color: rgba(255, 255, 255, 0.7);")  # Напівпрозорий фон
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setFixedHeight(20)
        info_label.setAttribute(Qt.WA_TranslucentBackground, True)

        # Додаємо layout з текстом до основного
        house_layout.addWidget(info_label, alignment=Qt.AlignTop)

    # Додаємо подію наведення
    def enterEvent(self, event):
        self.setStyleSheet("border: 2px solid blue;")
        super().enterEvent(event)

    # Подія коли курсор залишає віджет
    def leaveEvent(self, event):
        self.setStyleSheet("border: 1px solid black;")
        super().leaveEvent(event)

    # Обробка кліку
    def mousePressEvent(self, event):
        print(f"Clicked on {self.house.name}")
        self.open_stage_view()
        super().mousePressEvent(event)

    # Метод для відкриття вікна зі стадіями будинку
    def open_stage_view(self):
        from views.stage_view import StageViewWindow
        parent = self.parent()

        print(f"Opening stage view for house: {self.house.name}")
        stage_view = StageViewWindow(self.house, is_admin=parent.controller.is_admin)
        self.parent().close()
        stage_view.exec_()

        print("Closing parent window.")  # Додайте цю строку


# Запуск програми
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HouseGridWindow(is_admin=True)  # Встановіть is_admin=False для користувача
    window.show()
    sys.exit(app.exec_())
