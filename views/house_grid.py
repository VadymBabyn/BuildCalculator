import os

import stages as stages
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout, QLineEdit, QDialog, \
    QScrollBar, QScrollArea, QMenu, QAction, QSizePolicy, QMessageBox, QFileDialog, QGraphicsBlurEffect
from PyQt5.QtGui import QPixmap
from controller.house_controller import HouseController
import sys

from PyQt5.QtCore import Qt, QPropertyAnimation, QRect
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QGridLayout, QDialog, QLineEdit

from controller.matherial_controller import MatherialController
from controller.stage_controller import StageController
from controller.matherial_controller import MatherialController
from controller.matherial_purchased_controller import MatherialPurchasedController
from controller.payment_controller import PaymentController
from controller.sub_stage_controller import SubStageController


class HouseGridWindow(QDialog):
    def __init__(self, is_admin=False):
        super().__init__()
        self.setWindowTitle('Будинки')

        self.setStyleSheet("background-color: #f0f4f8;")  # Світло-сірий фон
        self.controller = HouseController(is_admin)
        self.stageController = StageController(is_admin)
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowMaximizeButtonHint |
                            Qt.WindowCloseButtonHint)
        # Головний макет
        main_layout = QVBoxLayout()
        # Вікно для прокручування
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Головний контейнер для сітки будинків
        self.grid_container = QWidget(self)
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)
        self.grid_layout.setSpacing(15)
        houses = self.controller.view_houses()
        row, col = 0, 0
        for house in houses:
            self.add_house_block(house, row, col)
            col += 1
            if col == 3:
                col = 0
                row += 1

        if is_admin:
            self.add_new_house_block(row, col)

        # Створюємо віджет для сітки
        #grid_widget = QWidget()
        #grid_widget.setLayout(self.grid_layout)

        # Додаємо віджет у ScrollArea
        scroll_area.setWidget(self.grid_container)

        # Додаємо scroll_area в головний макет
        main_layout.addWidget(scroll_area)

        self.background_label = QLabel(self)
        #self.background_label_grid = QLabel(self)
        self.set_grid_background()
        self.set_background()
        self.showMaximized()
        self.setLayout(main_layout)

    def set_grid_background(self):
        if getattr(sys, 'frozen', False):
            photo_path = sys._MEIPASS
        else:
            photo_path = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, 'frozen', False):
            photo_folder_path = os.path.join(photo_path, 'photo')
        else:
            photo_folder_path = os.path.join(photo_path, '..', 'photo')
        photo_file_path = os.path.join(photo_folder_path, 'backgroundImage3.jpg')
        """Встановлення фону для контейнера з сіткою."""
        pixmap = QPixmap(photo_file_path)  # замініть на шлях до вашого зображення
        scaled_pixmap = pixmap.scaled(self.grid_container.size(), Qt.KeepAspectRatioByExpanding)

        # Використання QLabel для фону
        if not hasattr(self, 'background_label_grid'):
            self.background_label_grid = QLabel(self.grid_container)
            blur_effect = QGraphicsBlurEffect()
            blur_effect.setBlurRadius(20)
            self.background_label_grid.setGraphicsEffect(blur_effect)
            self.background_label_grid.lower()  # Розташування фону за всіма іншими елементами

        self.background_label_grid.setPixmap(scaled_pixmap)
        self.background_label_grid.setGeometry(0, 0, self.grid_container.width(), self.grid_container.height())

    # Розташування фону за всіма іншими елементами

    def set_background(self):
        # Налаштування розмитого фону
        if getattr(sys, 'frozen', False):
            photo_path = sys._MEIPASS
        else:
            photo_path = os.path.dirname(os.path.abspath(__file__))
        if getattr(sys, 'frozen', False):
            photo_folder_path = os.path.join(photo_path, 'photo')
        else:
            photo_folder_path = os.path.join(photo_path, '..', 'photo')
        photo_file_path = os.path.join(photo_folder_path, 'BackgroundImage3.jpg')
        background_pixmap = QPixmap(photo_file_path)  # замініть на шлях до вашого зображення
        background_pixmap = background_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)

        # Встановлення фону
        self.background_label.setPixmap(background_pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())

        # Додавання ефекту розмиття
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.background_label.setGraphicsEffect(blur_effect)

        # Тримати фон на самому задньому плані
        self.background_label.lower()

  #

    def resizeEvent(self, event):
        """Обробка зміни розміру вікна."""
        super().resizeEvent(event)
        self.set_grid_background()
        self.set_background()

    def add_house_block(self, house, row, col):
        house_widget = ClickableHouseWidget(house, main_window=self)
        self.grid_layout.addWidget(house_widget, row, col)

    def add_new_house_block(self, row, col):
        new_house_layout = QVBoxLayout()

        add_button = QPushButton("+", self)
        add_button.setFixedSize(180, 180)
        add_button.setStyleSheet("""
               QPushButton {
                   background-color: #20be3f;  
                   color: white;
                   font-size: 28px;
                   border-radius: 12px;
               }
               QPushButton:hover {
                   background-color: #58e774;
               }
           """)
        # Додаємо кнопку з вирівнюванням по центру
        new_house_layout.addWidget(add_button, alignment=Qt.AlignCenter)

        # add_label = QLabel("Додати новий будинок", self)
        # add_label.setStyleSheet("color: #2a9d8f; font-size: 14px;")
        # add_label.setAlignment(Qt.AlignCenter)
        # new_house_layout.addWidget(add_label)

        # Додаємо макет до сітки
        self.grid_layout.addLayout(new_house_layout, row, col)

        # Зв'язуємо кнопку з дією
        add_button.clicked.connect(self.show_add_house_form)

    def show_add_house_form(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Додати новий будинок")

        layout = QVBoxLayout()
        name_input = QLineEdit(dialog)
        name_input.setPlaceholderText("Назва будинку")
        address_input = QLineEdit(dialog)
        address_input.setPlaceholderText("Адреса")
        floors_input = QLineEdit(dialog)
        floors_input.setPlaceholderText("Кількість поверхів")

        name_input.setStyleSheet("padding: 5px; border: 1px solid #a0a9b0; border-radius: 8px;")
        address_input.setStyleSheet("padding: 5px; border: 1px solid #a0a9b0; border-radius: 8px;")
        floors_input.setStyleSheet("padding: 5px; border: 1px solid #a0a9b0; border-radius: 8px;")

        layout.addWidget(name_input)
        layout.addWidget(address_input)
        layout.addWidget(floors_input)

        save_button = QPushButton("Зберегти", dialog)
        save_button.setStyleSheet("background-color: #20be3f; color: white; padding: 8px; border-radius: 10px;")
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
        if not name or not address or not floors or not floors.isdigit():
            QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть всі поля коректно.")
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
    def __init__(self, house, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.matherialController = MatherialController(is_admin=self.main_window.controller.is_admin)
        self.matherialPurchController = MatherialPurchasedController(is_admin=self.main_window.controller.is_admin)
        self.stageController = StageController(is_admin=self.main_window.controller.is_admin)
        self.subStageController = SubStageController(is_admin=self.main_window.controller.is_admin)
        self.paymentController = PaymentController(is_admin=self.main_window.controller.is_admin)
        self.houseController = HouseController(is_admin=self.main_window.controller.is_admin)
        self.house = house
        self.init_ui()

    def init_ui(self):
        # Основний контейнер
        house_layout = QVBoxLayout(self)
        house_layout.setContentsMargins(20, 20, 20, 20)  # Відступи
        house_layout.setSpacing(15)  # Простір між елементами

        # Фото будинку
        photo_label = QLabel(self)
        pixmap = QPixmap(self.house.photo)
        photo_label.setPixmap(pixmap.scaled(350, 350, aspectRatioMode=1))
        photo_label.setScaledContents(True)
        photo_label.setAlignment(Qt.AlignCenter)
        house_layout.addWidget(photo_label)

        # Інформаційний текст
        sub_stages = self.subStageController.view_all_sub_stages()
        stages = self.stageController.view_all_stages()
        suma_purch = 0
        total_cost = 0
        for stage in stages:
            if self.house.id == stage.id_stages_of_house:
                test_data = self.matherialController.view_matherial(stage.id_stages)
                test_data_purch = self.matherialPurchController.view_matherial(stage.id_stages)
                test_data_payment = self.paymentController.view_payment(stage.id_stages)
                for row_index, material in enumerate(test_data):
                    total_cost += material.sum
                for row_index, material in enumerate(test_data_purch):
                    suma_purch += material.sum
                for row_index, material in enumerate(test_data_payment):
                    suma_purch += material.sum
        for sub_stage in sub_stages:
            for stage in stages:
                if stage.id_stages == sub_stage.stages_id_stage and self.house.id == stage.id_stages_of_house:
                    test_data = self.matherialController.view_matherial(None, sub_stage.id_sub_stage)
                    test_data_purch = self.matherialPurchController.view_matherial(None, sub_stage.id_sub_stage)
                    test_data_payment = self.paymentController.view_payment(None, sub_stage.id_sub_stage)

                    for material in test_data:
                        total_cost += material.sum

                    for material in test_data_purch:
                        suma_purch += material.sum

                    for payment in test_data_payment:
                        suma_purch += payment.sum

        info_text = f"{self.house.name}\n{self.house.address}\nКількість поверхів: " \
                    f"{self.house.floors}\n Запланована сума: {total_cost} \n Потрачена сума: {suma_purch}"
        info_label = QLabel(info_text, self)
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet(
            """background-color: #D8F0F2; color: black; border-radius: 12px; padding: 10px;
             font-size: 24px; font-weight: bold; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);""")
        house_layout.addWidget(info_label)

        # Встановлюємо розміри віджету
        self.setFixedSize(500, 600)
        self.setStyleSheet(
            """ClickableHouseWidget { border: 1px solid #e0e0e0; border-radius: 15px;
             background-color: #f9f9f9; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);} 
             ClickableHouseWidget:hover { border: 2px solid #2a9d8f; background-color: #f1f1f1; }""")
        self.setLayout(house_layout)

    def show_context_menu(self, pos: QPoint):
        """Відображення контекстного меню для редагування та видалення."""
        menu = QMenu(self)
        makeReview = QAction("сформувати звіт", self)
        makeReview.triggered.connect(self.makereview)
        menu.addAction(makeReview)
        showChart = QAction("Показати діаграму", self)
        showChart.triggered.connect(self.showChart)
        menu.addAction(showChart)
        change_photo_action = QAction("змінити фото", self)
        change_photo_action.triggered.connect(self.change_photo)
        menu.addAction(change_photo_action)
        # Додати опції до меню
        edit_action = QAction("Редагувати", self)
        edit_action.triggered.connect(self.edit_house)
        menu.addAction(edit_action)

        delete_action = QAction("Видалити", self)
        delete_action.triggered.connect(self.delete_house)
        menu.addAction(delete_action)

        # Відображення меню у правильній позиції
        menu.exec_(self.mapToGlobal(pos))

    def makereview(self):
        from views.date_range_picker import DateRangePicker
        print(f"Opening stage view for house: {self.house.name}")
        stage_view = DateRangePicker()
        stage_view.show_date_picker(self.house.id)
      #  self.main_window.close()  # Закриваємо основне вікно
        stage_view.exec_()
        print("Closing parent window.")

    def showChart(self):
        from views.pie_chart_window import PieChartWindow
        print("Opening Diagram window")
        data = []
        stages = self.stageController.view_all_stages()
        sub_stages = self.subStageController.view_all_sub_stages()
        for stage in stages:
            if self.house.id == stage.id_stages_of_house:
                summa = 0
                summa_purch = 0

                test_data = self.matherialController.view_matherial(stage.id_stages)
                test_data_purch = self.matherialPurchController.view_matherial(stage.id_stages)
                test_data_payment = self.paymentController.view_payment(stage.id_stages)

                for material in test_data:
                    summa += material.sum

                for material in test_data_purch:
                    summa_purch += material.sum

                for payment in test_data_payment:
                    summa_purch += payment.sum

                data.append({
                    "stage": stage.stage_name,
                    "planned": int(summa),
                    "actual": int(summa_purch)
                })
        for sub_stage in sub_stages:
            for stage in stages:
                if stage.id_stages == sub_stage.stages_id_stage and self.house.id == stage.id_stages_of_house:
                    summa = 0
                    summa_purch = 0

                    test_data = self.matherialController.view_matherial(None, sub_stage.id_sub_stage)
                    test_data_purch = self.matherialPurchController.view_matherial(None, sub_stage.id_sub_stage)
                    test_data_payment = self.paymentController.view_payment(None, sub_stage.id_sub_stage)

                    for material in test_data:
                        summa += material.sum

                    for material in test_data_purch:
                        summa_purch += material.sum

                    for payment in test_data_payment:
                        summa_purch += payment.sum

                    data.append({
                        "stage": sub_stage.sub_stage_name,
                        "planned": int(summa),
                        "actual": int(summa_purch)
                    })

        pieChartWindow = PieChartWindow(data)
        pieChartWindow.exec_()

    def change_photo(self):
        # Відкрити діалог вибору файлу
        file_path, _ = QFileDialog.getOpenFileName(
            None,  # Вікно батько (None означає, що використовується головне вікно)
            "Виберіть фото",  # Заголовок діалогу
            "",  # Стартова директорія
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"  # Фільтр файлів
        )
        self.houseController.change_house_photo(self.house.id, file_path)
        # Якщо файл вибрано
        if file_path:
            self.main_window.refresh_grid()
            return file_path
        else:
            # Якщо користувач натиснув "Скасувати"
            QMessageBox.information(None, "Інформація", "Ви не вибрали файл.")
            return None

    def edit_house(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Редагувати будинок")

        layout = QVBoxLayout()
        name_input = QLineEdit(dialog)
        name_input.setText(self.house.name)
        address_input = QLineEdit(dialog)
        address_input.setText(self.house.address)
        floors_input = QLineEdit(dialog)
        floors_input.setText(str(self.house.floors))

        layout.addWidget(name_input)
        layout.addWidget(address_input)
        layout.addWidget(floors_input)

        save_button = QPushButton("Зберегти", dialog)
        save_button.setStyleSheet("""
                               QPushButton {
                                   background-color: #2a9d8f;  /* М'ятний колір */
                                   color: white;
                                   font-size: 24px;
                                   border-radius: 15px;
                               }
                               QPushButton:hover {
                                   background-color: #21867a;
                               }
                           """)
        layout.addWidget(save_button)

        save_button.clicked.connect(
            lambda: self.save_edited_house(name_input, address_input, floors_input, dialog))
        dialog.setLayout(layout)
        dialog.exec_()

    def save_edited_house(self, name_input, address_input, floors_input, dialog):
        if not name_input or not address_input or not floors_input or not floors_input.text().isdigit():
            QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть всі поля коректно.")
            print("Будь ласка, заповніть всі поля!")
            return
        self.house.name = name_input.text()
        self.house.address = address_input.text()
        self.house.floors = int(floors_input.text())

        self.main_window.controller.edit_house(self.house.id, self.house.name,  self.house.address, self.house.floors)
        self.main_window.refresh_grid()
        dialog.accept()

    def delete_house(self):
        confirm = QDialog(self)
        confirm.setWindowTitle("Підтвердження видалення")

        layout = QVBoxLayout()
        confirm_label = QLabel("Ви впевнені, що хочете видалити цей будинок?")
        layout.addWidget(confirm_label)

        button_layout = QVBoxLayout()
        yes_button = QPushButton("Так", confirm)
        no_button = QPushButton("Ні", confirm)
        yes_button.setStyleSheet("""
                       QPushButton {
                           background-color: Red;  /* М'ятний колір */
                           color: white;
                           font-size: 24px;
                           border-radius: 15px;
                       }
                       QPushButton:hover {
                           background-color: #790604;
                       }
                   """)
        no_button.setStyleSheet("""
                       QPushButton {
                           background-color: #2a9d8f;  /* М'ятний колір */
                           color: white;
                           font-size: 24px;
                           border-radius: 15px;
                       }
                       QPushButton:hover {
                           background-color: #21867a;
                       }
                   """)
        button_layout.addWidget(yes_button)
        button_layout.addWidget(no_button)
        layout.addLayout(button_layout)
        yes_button.clicked.connect(lambda: self.confirm_delete(confirm))
        no_button.clicked.connect(confirm.reject)

        confirm.setLayout(layout)
        confirm.exec_()

    def confirm_delete(self, dialog):
        self.main_window.controller.remove_house(self.house.id)
        self.main_window.refresh_grid()
        dialog.accept()

    def enterEvent(self, event):
        self.setStyleSheet("border: 2px solid #2a9d8f; background-color: #f7f7f7;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet("border: 1px solid #ddd; background-color: #ffffff;")
        super().leaveEvent(event)

    # Обробка кліку
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print(f"Clicked on {self.house.name}")
            self.open_stage_view()
            super().mousePressEvent(event)
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.pos())

    # Метод для відкриття вікна зі стадіями будинку
    def open_stage_view(self):
        from views.stage_view import StageViewWindow
        print(f"Opening stage view for house: {self.house.name}")
        stage_view = StageViewWindow(self.house, is_admin=self.main_window.controller.is_admin)
        self.main_window.close()  # Закриваємо основне вікно
        stage_view.exec_()
        print("Closing parent window.")  # Додайте цю строку


# Запуск програми
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HouseGridWindow(is_admin=True)  # Встановіть is_admin=False для користувача
    window.show()
    sys.exit(app.exec_())
