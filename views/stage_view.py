from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QGridLayout, QLineEdit, QDialog
from controller.stage_controller import StageController
import sys

class StageViewWindow(QDialog):
    def __init__(self, house=None, is_admin=False):
        super().__init__()
        self.house = house  # Зберігаємо дані про будинок
        self.is_admin = is_admin  # Зберігаємо роль користувача
        self.controller = StageController(is_admin)
        self.setWindowTitle('Етапи будівництва')
        self.setGeometry(100, 100, 800, 600)

        # Ініціалізація макету
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        # Показати інформацію про будинок, якщо доступна
        if self.house:
            self.show_house_info()

        # Отримати та відобразити етапи
        stages = self.controller.view_stages(self.house.id)
        self.add_stages_to_grid(stages)

        # Якщо адміністратор, додати кнопку "Додати новий етап"
        if self.is_admin:
            self.add_new_stage_button()

        # Додати кнопку "Назад"
        back_button = QPushButton("Назад", self)
        back_button.clicked.connect(self.back_to_house_grid)
        self.grid_layout.addWidget(back_button, self.grid_layout.rowCount(), 0, 1, 2)

    def show_house_info(self):
        # Відобразити інформацію про будинок
        house_info_label = QLabel(f"Будинок: {self.house.name}", self)
        self.grid_layout.addWidget(house_info_label)

    def add_stages_to_grid(self, stages):
        row = 0
        for stage in stages:
            stage_name_label = QLabel(stage.stage_name)
            self.grid_layout.addWidget(stage_name_label, row, 0)
            row += 1

    def add_new_stage_button(self):
        add_button = QPushButton("Додати новий етап")
        add_button.clicked.connect(self.add_new_stage_form)
        self.grid_layout.addWidget(add_button, self.grid_layout.rowCount(), 0, 1, 2)

    def add_new_stage_form(self):
        row = self.grid_layout.rowCount()
        stage_name_input = QLineEdit()
        stage_name_input.setPlaceholderText("Назва етапу")
        self.grid_layout.addWidget(stage_name_input, row, 0)

        save_button = QPushButton("Зберегти")
        save_button.clicked.connect(lambda: self.save_stage(stage_name_input))
        self.grid_layout.addWidget(save_button, row + 1, 0, 1, 2)

    def save_stage(self, stage_name_input):
        stage_name = stage_name_input.text()
        if stage_name:
            self.controller.add_new_stage(self.house.id, stage_name)
            stage_name_input.clear()
            self.update_stages()
        else:
            print("Будь ласка, заповніть всі поля.")

    def update_stages(self):
        # Очистити сітку етапів
        for i in range(self.grid_layout.rowCount() - 2):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Отримати нові етапи та додати їх до сітки
        stages = self.controller.view_stages(self.house.id)
        self.add_stages_to_grid(stages)

    def back_to_house_grid(self):
        from views.house_grid import HouseGridWindow
        self.home_page = HouseGridWindow(is_admin=self.is_admin)
        self.close()
        self.home_page.exec_()

# Запуск програми
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StageViewWindow(is_admin=True)  # Змініть на is_admin=False для звичайного користувача
    window.show()
    sys.exit(app.exec_())
