import os

from PyQt5.QtCore import Qt, QPoint, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QDialog,
    QWidget,
    QSpacerItem,
    QSizePolicy, QMenu, QAction, QHBoxLayout, QStyle, QInputDialog, QMessageBox, QGraphicsBlurEffect, QScrollArea
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
import sys

from controller.matherial_controller import MatherialController
from controller.matherial_purchased_controller import MatherialPurchasedController
from controller.payment_controller import PaymentController
from controller.stage_controller import StageController
from controller.sub_stage_controller import SubStageController
class StageLabel(QLabel):
    """Кастомний QLabel з обробкою правого кліку (контекстне меню)"""
    def __init__(self, stage_name, stage_id, parent=None, is_admin=False):
        super().__init__(stage_name, parent)
        self.stage_name = stage_name
        self.stage_id = stage_id
        self.is_admin = is_admin
        self.parent = parent
        self.matherialController = MatherialController(is_admin=self.is_admin)
        self.matherialPurchController = MatherialPurchasedController(is_admin=self.is_admin)
        self.paymentController = PaymentController(is_admin=self.is_admin)
    def mousePressEvent(self, event):
        """ Обробка натискання миші """
        if event.button() == Qt.RightButton:
            self.show_context_menu(event.globalPos())  # Відкрити контекстне меню
        elif event.button() == Qt.LeftButton:
            self.toggle_substages(self.stage_id)
        else:
            super().mousePressEvent(event)

    def show_context_menu(self, global_pos: QPoint):
        """ Відкриває контекстне меню при кліку правою кнопкою миші """
        menu = QMenu(self)
        add_subgroup_action = QAction("Додати підгрупу", self)
        add_subgroup_action.triggered.connect(self.show_add_subgroup_dialog)
        menu.addAction(add_subgroup_action)
        show_chart = QAction("Переглянути діаграму", self)
        show_chart.triggered.connect(self.show_stage_detail_chart)
        menu.addAction(show_chart)
        menu.exec_(global_pos)

    def show_add_subgroup_dialog(self):
        """ Відкриває діалогове вікно для введення підгрупи """
        dialog = AddSubgroupDialog(self.stage_name, self.stage_id, self, self.is_admin)
        dialog.exec_()

    def show_stage_detail_chart(self):
        """ Відкриває вікно з трьома діаграмами: матеріали заплановані, фактичні, послуги """
        from views.detail_chart_window import SingleStageDetailChartWindow  # або правильний шлях

        # Отримуємо дані по матеріалах та послугах для поточного етапу
        materials = []
        planned = self.matherialController.view_matherial(self.stage_id)
        actuals = self.matherialPurchController.view_matherial(self.stage_id)
        services = self.paymentController.view_payment(self.stage_id)

        # Індекс по назві матеріалу
        material_map = {}

        for mat in planned:
            material_map[mat.matherial_name] = {"name": mat.matherial_name, "planned": mat.sum, "actual": 0}

        for mat in actuals:
            if mat.matherial_name in material_map:
                material_map[mat.matherial_name]["actual"] += mat.sum
            else:
                material_map[mat.matherial_name] = {"name": mat.matherial_name, "planned": 0, "actual": mat.sum}

        materials = list(material_map.values())

        service_data = []
        for srv in services:
            service_data.append({
                "name": srv.matherial_name,
                "amount": srv.sum
            })

        stage_data = {
            "materials": materials,
            "services": service_data
        }

        chart_window = SingleStageDetailChartWindow(stage_data)
        chart_window.exec_()

    def toggle_substages(self, stage_id):
        StageViewWindow.toggle_substages(self.parent, stage_id)



class AddSubgroupDialog(QDialog):
    """ Діалогове вікно для додавання підгрупи """
    def __init__(self, stage_name, stage_id, parent=None, is_admin=False):
        super().__init__(parent)
        self.setWindowTitle(f"Додати підгрупу до {stage_name}")
        self.stage_name = stage_name
        self.stage_id = stage_id
        self.sub_stage_controller = SubStageController(is_admin)
        layout = QVBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Введіть назву підгрупи")
        layout.addWidget(self.input_field)

        self.save_button = QPushButton("Зберегти", self)
        self.save_button.clicked.connect(self.save_subgroup)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_subgroup(self):
        """Зберегти підгрупу"""
        subgroup_name = self.input_field.text().strip()
        if not subgroup_name:
            QMessageBox.warning(self, "Помилка", "Назва підгрупи не може бути порожньою!")
            return
        self.sub_stage_controller.add_new_sub_stage(self.stage_id, subgroup_name)
        QMessageBox.information(self, "Успіх", f"Підгрупа '{subgroup_name}' додана до етапу '{self.stage_name}'")
        self.accept()

class StageViewWindow(QDialog):
    def __init__(self, house=None, is_admin=False):
        super().__init__()
        self.house = house
        self.is_admin = is_admin
        self.stage_controller = StageController(is_admin)
        self.sub_stage_controller = SubStageController(is_admin)
        self.setWindowTitle('Етапи будівництва')
        self.setGeometry(100, 100, 800, 600)
        self.is_stage_form_visible = False
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowMaximizeButtonHint |
                            Qt.WindowCloseButtonHint)
        # **Додавання сучасного вигляду (шрифти, стилі)**
        self.setStyleSheet(self._get_styles())
        # Ініціалізація основного макета
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)

        # Інформація про будинок
        if self.house:
            house_info_label = QLabel(f"Будинок: {self.house.name}", self)
            house_info_label.setFont(QFont("Arial", 16, QFont.Bold))
            main_layout.addWidget(house_info_label)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setObjectName("scrollArea")
        # Макет для сітки етапів

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(15)
        self.grid_layout.setAlignment(Qt.AlignTop)

        self.stage_widgets = {}
        self.substage_container = QWidget()
        self.substage_layout = QHBoxLayout(self.substage_container)

        grid_widget = QWidget()
        grid_widget.setLayout(self.grid_layout)
        grid_widget.setObjectName("scrollContainer")

        scroll_area.setWidget(grid_widget)
        main_layout.addWidget(scroll_area)

        main_layout.setStretchFactor(scroll_area, 1)
        self.background_label = QLabel(self)
        # Кнопки управління в окремому контейнері
        self.add_control_buttons(main_layout)
        self.set_background()
        # Отримати та відобразити етапи
        self.update_stages()
        self.showMaximized()

    def _get_styles(self):
        """Метод для визначення стилів."""
        return """
        QDialog {
            background-color: #F5F5F5;
        }
        
        QLabel {
            font-size: 32px;
            color: black;
            background-color: #a7a7b4;
            border-radius: 6px;
        }
        QPushButton {
            font-size: 24px;
            padding: 10px 15px;
            background-color: #e0e0e1;
            color: black;
            border: none;
            border-radius: 8px;
        }
        QPushButton:hover {
            background-color: #95F1FA;
        }
        QLineEdit {
            font-size: 24px;
            padding: 8px;
            border: 2px solid #CCC;
            border-radius: 6px;
            margin-bottom: 10px;
        }
        QPushButton#deleteButton {
            background-color: #D9534F;
        }
        QPushButton#deleteButton:hover {
            background-color: #C9302C;
        }
        /* Прозорий фон для QScrollArea */
        QScrollArea#scrollArea {
            background: transparent;
            border: none;
        }
        /* Прозорий фон для віджета всередині QScrollArea */
        QWidget#scrollContainer {
            background: transparent;
        }
        """

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

    def resizeEvent(self, event):
        """Обробка зміни розміру вікна."""
        super().resizeEvent(event)
        self.set_background()

    def add_stages_to_grid(self, stages):
        # Очистка сітки
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Заголовки
        headers = ["Назва етапу", "Заплановано", "Куплено", "Послуги", "Докупити"]
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setAlignment(Qt.AlignCenter)
            header_label.setFixedHeight(40)
            self.grid_layout.addWidget(header_label, 0, col)

        row = 1  # Лічильник рядків

        # Додавання етапів
        for stage in stages:
            stage_label = StageLabel(stage.stage_name, stage.id_stages, self, self.is_admin)
            self.grid_layout.addWidget(stage_label, row, 0)

            # Контейнер для підгруп (початково прихований)
            substage_container = QWidget()
            substage_layout = QVBoxLayout(substage_container)
            substage_layout.setContentsMargins(20, 5, 5, 5)
            substage_container.setLayout(substage_layout)
            substage_container.setVisible(False)
            substage_container.setStyleSheet("background-color: transparent")
            self.grid_layout.addWidget(substage_container, row + 1, 0, 1, -1)

            self.stage_widgets[stage.id_stages] = substage_container



            # Збільшуємо row_counter після основного етапу


            planned_button = QPushButton("Заплановано")
            planned_button.setStyleSheet("""
               QPushButton {
                   background-color: #bcbcc2;  
                   color: black;
                   font-size: 24px;
                   border-radius: 12px;
               }
               QPushButton:hover {
                   background-color: #66B8D9;
               }
           """)
            planned_button.clicked.connect(lambda checked, s=stage: self.mark_stage_as_planned(s))
            self.grid_layout.addWidget(planned_button, row, 1)

            purchased_button = QPushButton("Куплено")
            purchased_button.clicked.connect(lambda checked, s=stage: self.mark_stage_as_purchased(s))
            self.grid_layout.addWidget(purchased_button, row, 2)

            purchased_button = QPushButton("Послуги")
            purchased_button.setStyleSheet("""
               QPushButton {
                   background-color: #bcbcc2;  
                   color: black;
                   font-size: 24px;
                   border-radius: 12px;
               }
               QPushButton:hover {
                   background-color: #66B8D9;
               }
           """)
            purchased_button.clicked.connect(lambda checked, s=stage: self.mark_stage_as_to_payment(s))
            self.grid_layout.addWidget(purchased_button, row, 3)

            to_buy_button = QPushButton("Докупити")
            to_buy_button.clicked.connect(lambda checked, s=stage: self.mark_stage_as_to_buy(s))
            self.grid_layout.addWidget(to_buy_button, row, 4)
            # Кнопки для дій
            actions_layout = QHBoxLayout()

            # Кнопка редагування
            edit_button = QPushButton()
            edit_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)  # Іконка редагування
            edit_button.setIcon(edit_icon)
            edit_button.setToolTip("Редагувати")
            edit_button.clicked.connect(lambda checked, s=stage: self.edit_stage(s))
            actions_layout.addWidget(edit_button)

            # Кнопка видалення
            delete_button = QPushButton()
            delete_icon = self.style().standardIcon(QStyle.SP_TrashIcon)  # Іконка видалення
            delete_button.setIcon(delete_icon)
            delete_button.setToolTip("Видалити")
            delete_button.clicked.connect(lambda checked, s=stage: self.delete_stage(s))
            delete_button.setStyleSheet("""
               QPushButton {
                   background-color: red;  
               }
               QPushButton:hover {
                   background-color: #b52121;
               }
           """)
            actions_layout.addWidget(delete_button)

            # Додавання дій у сітку
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            actions_widget.setStyleSheet("""
                QWidget {
                    background-color: Transparent; /* Світло-сірий фон */
                }
                QPushButton {
                    background-color: #468BA6;  
                    color: white;
                    font-size: 24px;
                    border-radius: 12px;
                    padding: 10px 20px; /* Додає внутрішній відступ */
                    border: 2px solid #3A7F92; /* Додає тонкий контур */
                }
                QPushButton:hover {
                    background-color: #66B8D9; /* Світліший колір при наведенні */
                    border: 2px solid #5BA3BD; /* Зміна кольору контуру */
                }
                QPushButton:pressed {
                    background-color: #3A7F92; /* Темніший колір при натисканні */
                    border: 2px solid #2F687A; /* Темніший контур */
                }
            """)
            self.grid_layout.addWidget(actions_widget, row, 5)

            # Додатковий простір у клітинках для гнучкості
            self.grid_layout.setColumnStretch(0, 2)
            self.grid_layout.setColumnStretch(1, 1)
            self.grid_layout.setColumnStretch(2, 1)
            self.grid_layout.setColumnStretch(3, 1)
            self.grid_layout.setColumnStretch(4, 1)
            # Додаємо підгрупи
            substages = self.sub_stage_controller.view_sub_stages(stage.id_stages)
            if substages:
                for substage in substages:
                    sub_label = QLabel(f"  ➤ {substage.sub_stage_name}")
                    substage_layout.addWidget(sub_label)

                # Оновлюємо row_counter, щоб наступний етап був після всіх підгруп
                row += len(substages)
            row += 1

    def toggle_substages(self, stage_id):
        """Перемикає видимість підгруп"""
        if stage_id in self.stage_widgets:
            is_visible = self.stage_widgets[stage_id].isVisible()
            self.stage_widgets[stage_id].setVisible(not is_visible)

            if not is_visible:  # Якщо підгрупи тільки що розгорнулись, завантажуємо їх
                self.load_substages(stage_id)

            # Оновлюємо макет після зміни видимості
           #

    def load_substages(self, stage_id):
        """Завантажує підгрупи для певного етапу"""
        self.substage_container = self.stage_widgets[stage_id]
        self.substage_layout = self.substage_container.layout()

        # Очищаємо попередній список підгруп
        while self.substage_layout.count():
            item = self.substage_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sub_stages = self.sub_stage_controller.view_sub_stages(stage_id)

        for sub_stage in sub_stages:
            # Основний контейнер для рядка
            row_widget = QWidget()
            row_layout = QHBoxLayout(row_widget)
            row_layout.setContentsMargins(5, 2, 5, 2)  # Внутрішні відступи
            row_layout.setSpacing(15)  # Відступи між елементами

            # Назва підгрупи

            sub_label = QLabel(f"  ➤ {sub_stage.sub_stage_name}")
            sub_label.setWordWrap(True)  # Включаємо автоматичний перенос
            sub_label.setMinimumWidth(520)
            sub_label.setMaximumWidth(520)  # Запобігає надмірному розширенню
            sub_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)  # Авто-зміна висоти
            sub_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Вирівнюємо текст зверху
            sub_label.setStyleSheet("font-size: 32px;color: black;background-color: #a7a7c1;border-radius: 6px;")

            row_layout.addWidget(sub_label)
            sub_label.adjustSize()

            # Додавання кнопок
            planned_button = QPushButton("Заплановано")
            planned_button.setMinimumWidth(200)
            planned_button.setStyleSheet("""
               QPushButton {
                   background-color: #bcbcc2;  
                   color: black;
                   font-size: 24px;
                   border-radius: 12px;
               }
               QPushButton:hover {
                   background-color: #66B8D9;
               }
           """)
            planned_button.clicked.connect(lambda checked, s=sub_stage: self.mark_stage_as_planned(None, s))

            purchased_button = QPushButton("Куплено")
            purchased_button.setMinimumWidth(200)
            purchased_button.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    padding: 10px 15px;
                    background-color: #e0e0e1;
                    color: black;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #95F1FA;
                }
           """)
            purchased_button.clicked.connect(lambda checked, s=sub_stage: self.mark_stage_as_purchased(None, s))

            services_button = QPushButton("Послуги")
            services_button.setMinimumWidth(200)
            services_button.setStyleSheet("""
               QPushButton {
                   background-color: #bcbcc2;  
                   color: black;
                   font-size: 24px;
                   border-radius: 12px;
               }
               QPushButton:hover {
                   background-color: #66B8D9;
               }
           """)
            services_button.clicked.connect(lambda checked, s=sub_stage: self.mark_stage_as_to_payment(None, s))

            to_buy_button = QPushButton("Докупити")
            to_buy_button.setMinimumWidth(200)
            to_buy_button.setStyleSheet("""
                QPushButton {
                    font-size: 24px;
                    padding: 10px 15px;
                    background-color: #e0e0e1;
                    color: black;
                    border: none;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #95F1FA;
                }
            """)
            to_buy_button.clicked.connect(lambda checked, s=sub_stage: self.mark_stage_as_to_buy(None, s))

            # Додаємо кнопки в ряд
            row_layout.addWidget(planned_button)
            row_layout.addWidget(purchased_button)
            row_layout.addWidget(services_button)
            row_layout.addWidget(to_buy_button)

            # Кнопки редагування та видалення
            edit_button = QPushButton()
            edit_icon = self.style().standardIcon(QStyle.SP_FileDialogDetailedView)
            edit_button.setIcon(edit_icon)
            edit_button.setMaximumWidth(70)
            edit_button.setToolTip("Редагувати")
            edit_button.clicked.connect(lambda checked, s=sub_stage: self.edit_stage(None, s))
            edit_button.setStyleSheet("""
               QPushButton {
                   font-size: 24px;
                   padding: 10px 15px;
                   background-color: #e0e0e1;
                   color: black;
                   border: none;
                   border-radius: 8px;
               }
               QPushButton:hover {
                   background-color: #95F1FA;
               }
           """)
            delete_button = QPushButton()
            delete_icon = self.style().standardIcon(QStyle.SP_TrashIcon)
            delete_button.setIcon(delete_icon)
            delete_button.setMaximumWidth(70)
            delete_button.setToolTip("Видалити")
            delete_button.clicked.connect(lambda checked, s=sub_stage: self.delete_stage(None, s))
            delete_button.setStyleSheet("""
                QPushButton {
                    background-color: red;  
                }
                QPushButton:hover {
                    background-color: #b52121;
                }
            """)
            actions_layout = QHBoxLayout()
            # Додавання дій у сітку
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(delete_button)
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            actions_widget.setMaximumWidth(150)
            actions_widget.setStyleSheet("""
                            QWidget {
                                background-color: Transparent; /* Світло-сірий фон */
                            }
                            QPushButton {
                                background-color: #468BA6;  
                                color: white;
                                font-size: 24px;
                                border-radius: 12px;
                                padding: 10px 20px; /* Додає внутрішній відступ */
                                border: 2px solid #3A7F92; /* Додає тонкий контур */
                            }
                            QPushButton:hover {
                                background-color: #66B8D9; /* Світліший колір при наведенні */
                                border: 2px solid #5BA3BD; /* Зміна кольору контуру */
                            }
                            QPushButton:pressed {
                                background-color: #3A7F92; /* Темніший колір при натисканні */
                                border: 2px solid #2F687A; /* Темніший контур */
                            }
                        """)
            # Додаємо кнопки в ряд
            row_layout.addWidget(actions_widget)

            # Додаємо готовий рядок у layout підгруп
            self.substage_layout.addWidget(row_widget)

    def update_stages(self):
        # Очищення сітки для етапів (залишаємо управління)
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Знову отримати та додати етапи
        stages = self.stage_controller.view_stages(self.house.id)
        self.add_stages_to_grid(stages)

    def edit_stage(self, stage=None, sub_stage=None):
        if stage:
            new_name, ok = QInputDialog.getText(self, "Редагувати етап", "Введіть нову назву етапу:", QLineEdit.Normal,
                                                stage.stage_name)
            if ok and new_name:
                self.stage_controller.edit_stage(stage.id_stages, new_name)
                self.update_stages()
        elif sub_stage:
            new_name, ok = QInputDialog.getText(self, "Редагувати етап", "Введіть нову назву етапу:", QLineEdit.Normal,
                                                sub_stage.sub_stage_name)
            if ok and new_name:
                self.sub_stage_controller.edit_sub_stage(sub_stage.id_sub_stage, new_name)
                self.update_stages()

    def delete_stage(self, stage=None, sub_stage=None):
        if stage:
            reply = QMessageBox.question(self, "Підтвердження видалення",
                                         f"Ви впевнені, що хочете видалити етап '{stage.stage_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.stage_controller.remove_stage(stage.id_stages)
                self.update_stages()
        elif sub_stage:
            reply = QMessageBox.question(self, "Підтвердження видалення",
                                         f"Ви впевнені, що хочете видалити етап '{sub_stage.sub_stage_name}'?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.sub_stage_controller.remove_sub_stage(sub_stage.id_sub_stage)
                self.update_stages()


    def mark_stage_as_planned(self, stage=None, sub_stage=None):
        from views.matherial_view import MaterialView
        if stage:
            print(f"Stage '{stage.stage_name}' marked as 'Заплановано'")
            matherial_view = MaterialView(stage=stage, sub_stage=None, table_as="planned", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")
        elif sub_stage:
            print(f"Stage '{sub_stage.sub_stage_name}' marked as 'Заплановано'")
            matherial_view = MaterialView(stage=None, sub_stage = sub_stage, table_as="planned", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")

    def mark_stage_as_purchased(self, stage=None, sub_stage=None):
        from views.matherial_view import MaterialView
        if stage:
            print(f"Stage '{stage.stage_name}' marked as 'Куплено'")
            matherial_view = MaterialView(stage=stage, sub_stage=None, table_as="purchased", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")
        elif sub_stage:
            print(f"Stage '{sub_stage.sub_stage_name}' marked as 'Куплено'")
            matherial_view = MaterialView(stage=None, sub_stage=sub_stage, table_as="purchased", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")

    def mark_stage_as_to_payment(self, stage=None, sub_stage=None):
        from views.matherial_view import MaterialView
        if stage:
            print(f"Stage '{stage.stage_name}' marked as 'Послуги'")
            matherial_view = MaterialView(stage=stage,sub_stage=None, table_as="payment", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")
        elif sub_stage:
            print(f"Stage '{sub_stage.sub_stage_name}' marked as 'Послуги'")
            matherial_view = MaterialView(stage=None, sub_stage=sub_stage, table_as="payment", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")

    def mark_stage_as_to_buy(self, stage=None, sub_stage=None):
        from views.matherial_view import MaterialView
        if stage:
            print(f"Stage '{stage.stage_name}' marked as 'Докупити'")
            matherial_view = MaterialView(stage=stage,sub_stage=None, table_as="to_buy", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()
            print("Material view closed.")
        elif sub_stage:
            print(f"Stage '{sub_stage.sub_stage_name}' marked as 'Докупити'")
            matherial_view = MaterialView(stage=None, sub_stage=sub_stage, table_as="to_buy", is_admin=self.is_admin)

            # Замість закриття батьківського вікна, просто запустіть матеріал вікно

            matherial_view.exec_()

            print("Material view closed.")


    def add_control_buttons(self, main_layout):
        control_layout = QVBoxLayout()

        # Простір між елементами
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопка додавання
        if self.is_admin:
            self.add_button = QPushButton("Додати новий етап")
            self.add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            self.add_button.clicked.connect(self.add_new_stage_form)
            control_layout.addWidget(self.add_button)

        # Кнопка "Назад"
        self.back_button = QPushButton("Назад", self)
        self.back_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.back_button.clicked.connect(self.back_to_house_grid)
        control_layout.addWidget(self.back_button)

        # Простір внизу
        control_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        main_layout.addLayout(control_layout)

    def add_new_stage_form(self):
        if self.is_stage_form_visible:
            return

        self.stage_name_input = QLineEdit()
        self.stage_name_input.setPlaceholderText("Назва етапу")
        self.grid_layout.addWidget(self.stage_name_input, self.grid_layout.rowCount(), 0)

        self.save_button = QPushButton("Зберегти")
        self.save_button.clicked.connect(lambda: self.save_stage(self.stage_name_input))
        self.grid_layout.addWidget(self.save_button, self.grid_layout.rowCount(), 0)

        self.is_stage_form_visible = True

    def save_stage(self, stage_name_input):
        stage_name = stage_name_input.text()
        if stage_name:
            self.stage_controller.add_new_stage(self.house.id, stage_name)
            self.is_stage_form_visible = False
            stage_name_input.clear()
            self.update_stages()
        else:
            print("Будь ласка, заповніть всі поля.")



    def back_to_house_grid(self):
        from views.house_grid import HouseGridWindow
        self.home_page = HouseGridWindow(is_admin=self.is_admin)
        self.close()
        self.home_page.exec_()


# Запуск програми
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StageViewWindow(is_admin=True)
    window.show()
    sys.exit(app.exec_())
