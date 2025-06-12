from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QDialog, QMessageBox, QHeaderView, QPushButton,
    QLineEdit, QFormLayout, QHBoxLayout
)
from controller.matherial_controller import MatherialController
from controller.matherial_purchased_controller import MatherialPurchasedController
from controller.history_controller import HistoryController
from controller.payment_controller import PaymentController
import sys

class PurchaseDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Докупити матеріал")
        self.resize(300, 150)

        self.amount_input = QLineEdit()
        self.price_input = QLineEdit()
        self.provider_input = QLineEdit()

        layout = QFormLayout()
        layout.addRow("Кількість:", self.amount_input)
        layout.addRow("Ціна:", self.price_input)
        layout.addRow("Постачальник:", self.provider_input)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Скасувати")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        try:
            amount = float(self.amount_input.text())
            price = float(self.price_input.text())
            provider = self.provider_input.text()
            return amount, price, provider
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть коректні числові значення.")
            return None, None, None

class PaymentDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Оплата послуг")
        self.resize(300, 150)

        self.amount_input = QLineEdit()
        self.price_input = QLineEdit()
        self.payment_input = QLineEdit()

        layout = QFormLayout()
        layout.addRow("Кількість:", self.amount_input)
        layout.addRow("Ціна:", self.price_input)
        layout.addRow("Отримувач:", self.payment_input)

        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Скасувати")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout.addRow(button_layout)
        self.setLayout(layout)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_data(self):
        try:
            amount = float(self.amount_input.text())
            price = float(self.price_input.text())
            payment = self.payment_input.text()
            return amount, price, payment
        except ValueError:
            QMessageBox.warning(self, "Помилка", "Будь ласка, введіть коректні числові значення.")
            return None, None, None

class MaterialView(QDialog):
    def __init__(self, stage=None, sub_stage=None, table_as="", is_admin=False, matherial_id=None, payments_id=None):
        super().__init__()
        self.stage = stage
        self.sub_stage = sub_stage
        self.table_as = table_as
        self.is_admin = is_admin
        self.matheriales_id = matherial_id
        self.paymentes_id = payments_id
        self.setWindowTitle("Material View" + " " + table_as)
        self.resize(800, 400)
        self.matherialController = MatherialController(is_admin)
        self.matherialPurchController = MatherialPurchasedController(is_admin)
        self.historyController = HistoryController(is_admin)
        self.paymentController = PaymentController(is_admin)
        self.updating_table = False  # Додаємо прапорець для уникнення зайвих оновлень
        self.setWindowFlags(self.windowFlags() |
                            Qt.WindowMinimizeButtonHint |
                            Qt.WindowMaximizeButtonHint |
                            Qt.WindowCloseButtonHint)

        # Створюємо таблицю
        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Кількість колонок
        self.table.setHorizontalHeaderLabels(["Назва матеріалу", "од. вимір.", "Кількість", "Ціна", "Сумма", "Дія"])
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)

        # Підключаємо сигнал до обробника зміни даних в комірках
        self.table.cellChanged.connect(self.on_cell_changed)

        # Заповнюємо таблицю даними
        self.populate_table()

        # Розміщуємо таблицю в макеті
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.showMaximized()
        self.setLayout(layout)

    def on_cell_changed(self, row, column):
        if self.updating_table:
            return  # Якщо таблиця оновлюється, то нічого не робимо

        if row == self.table.rowCount() - 1:
            # Якщо це новий рядок, перевіряємо, чи заповнені всі необхідні поля
            if self.is_row_filled(row) and (self.table_as == "planned" or self.table_as == "payment"):
                if self.validate_row(row):
                    self.add_new_material(row)
                else:
                    QMessageBox.warning(self, "Помилка", "Будь ласка, заповніть всі поля коректно.")
                    self.populate_table()
        else:
            # Оновлення існуючого матеріалу
            if self.is_row_filled(row):
                if self.validate_row(row):
                    self.update_material(row)
                else:
                    self.populate_table()

    def is_row_filled(self, row):
        # Перевірка, чи заповнені всі клітинки в рядку
        if self.table_as == "payment":
            for col in range(self.table.columnCount() - 4):
                item = self.table.item(row, col)
                if not item or not item.text().strip():
                    return False
        else:
            for col in range(self.table.columnCount() - 2):
                item = self.table.item(row, col)
                if not item or not item.text().strip():
                    return False
        return True

    def validate_row(self, row):
        # Валідація введених даних
        try:
            matherial_name = self.table.item(row, 0).text()
            unit = self.table.item(row, 1).text()
            amount = float(self.table.item(row, 2).text())
            price = float(self.table.item(row, 3).text())
            return matherial_name.__len__() < 65 and unit.__len__() < 25 and amount >= 0 and price >= 0
            # Кількість і ціна повинні бути додатніми
        except ValueError:
            return False  # Повернути False, якщо не числові значення

    def add_new_material(self, row):
        # Збереження нового матеріалу в базу даних
        material_name = self.table.item(row, 0).text()
        unit = self.table.item(row, 1).text()
        amount = float(self.table.item(row, 2).text())
        price = float(self.table.item(row, 3).text())
        total_sum = amount * price
        if self.table_as == "planned":
            if self.stage:
                self.matherialController.add_new_matherial(material_name, unit, amount, price, self.stage.id_stages,)
            elif self.sub_stage:
                self.matherialController.add_new_matherial(material_name, unit, amount, price, None, self.sub_stage.id_sub_stage)
        elif self.table_as == "payment":
            if self.stage:
                self.paymentController.add_new_payment(self.stage.id_stages, None, None, material_name, unit, amount, price)
            elif self.sub_stage:
                self.paymentController.add_new_payment(None, self.sub_stage.id_sub_stage, None, material_name, unit, amount, price)
        self.populate_table()

    def update_material(self, row):
        # Оновлення даних матеріалу в базі
        if self.table_as == "planned":
            if self.stage:
                test_data = self.matherialController.view_matherial(self.stage.id_stages, None)
            else:
                test_data = self.matherialController.view_matherial(None, self.sub_stage.id_sub_stage)
            material_id = test_data[row].id_matherial
            material_name = self.table.item(row, 0).text()
            unit = self.table.item(row, 1).text()
            amount = float(self.table.item(row, 2).text())
            price = float(self.table.item(row, 3).text())
            self.matherialController.edit_matherial(material_id, material_name, unit, amount, price)
            if self.stage:
                test_data_pur = self.matherialPurchController.view_matherial(self.stage.id_stages,None)
            else:
                test_data_pur = self.matherialPurchController.view_matherial(None, self.sub_stage.id_sub_stage)
            material_id_pur = test_data_pur[row].id_matherial
            material_name_pur = self.table.item(row, 0).text()
            unit_pur = self.table.item(row, 1).text()
            amount_pur = float(self.table.item(row, 2).text())
            price_pur = float(self.table.item(row, 3).text())
            sum_pur = float(self.table.item(row, 4).text())
            self.matherialPurchController.edit_matherial(material_id_pur, material_name_pur, unit_pur, amount_pur,
                                                         price_pur, sum_pur, self.table_as)
        elif self.table_as == "purchased":
            if self.stage:
                test_data = self.matherialPurchController.view_matherial(self.stage.id_stages, None)
            else:
                test_data = self.matherialPurchController.view_matherial(None, self.sub_stage.id_sub_stage)
            material_id = test_data[row].id_matherial
            material_name = self.table.item(row, 0).text()
            unit = self.table.item(row, 1).text()
            amount = float(self.table.item(row, 2).text())
            price = float(self.table.item(row, 3).text())
            sum_pur = float(self.table.item(row, 4).text())
            self.matherialPurchController.edit_matherial(material_id, material_name, unit, amount, price, sum_pur)
        elif self.table_as == "payment":
            if self.stage:
                test_data = self.paymentController.view_payment(self.stage.id_stages)
            else:
                test_data = self.paymentController.view_payment(None, self.sub_stage.id_sub_stage)
            payment_id = test_data[row].id_payment
            material_name = self.table.item(row, 0).text()
            unit = self.table.item(row, 1).text()
            amount = float(self.table.item(row, 2).text())
            price = float(self.table.item(row, 3).text())
            sum_pur = float(self.table.item(row, 4).text())
            self.paymentController.edit_payment(payment_id, material_name, unit, amount, price, sum_pur,self.table_as)
        self.populate_table()

    def showHistoryTable(self, matherial_id=None,payment_id=None):

        matherial_view = MaterialView(stage=None, table_as="history", is_admin=self.is_admin, matherial_id=matherial_id, payments_id=payment_id)

        # Замість закриття батьківського вікна, просто запустіть матеріал вікно

        matherial_view.exec_()

    def open_purchase_dialog(self, row, test_data):
        dialog = PurchaseDialog()
        if dialog.exec_():
            amount, price, provider = dialog.get_data()
            if amount is not None and price is not None:
                self.process_purchase(row, test_data, amount, price, provider)

    def process_purchase(self, row, test_data, amount, price, provider):
        if self.stage:
            test_data_purch = self.matherialPurchController.view_matherial(self.stage.id_stages)
        else:
            test_data_purch = self.matherialPurchController.view_matherial(None, self.sub_stage.id_sub_stage)
        # Обробка даних докупівлі
        try:
            self.historyController.add_new_history(provider, test_data_purch[row].unit, amount,
                                                   price, test_data_purch[row].sum,
                                                   test_data_purch[row].id_matherial)
            self.matherialPurchController.purchase_matherial(test_data[row].id_matherial, amount, price)
            self.populate_table()
            QMessageBox.information(self, "Успіх", "Матеріал докуплено успішно.")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Сталася помилка: {e}")

    def open_payment_dialog(self, row, test_data):
        dialog = PaymentDialog()
        if dialog.exec_():
            amount, price, payment = dialog.get_data()
            if amount is not None and price is not None:
                self.process_payment(row, test_data, amount, price, payment)

    def process_payment(self, row, test_data, amount, price, payment):
        if self.stage:
            test_data_payment = self.paymentController.view_payment(self.stage.id_stages)
        else:
            test_data_payment = self.paymentController.view_payment(None,self.sub_stage.id_sub_stage)
        # Обробка даних докупівлі
        try:
            self.historyController.add_new_history(payment, test_data_payment[row].unit, amount,
                                                   price, test_data_payment[row].sum,
                                                   None, test_data_payment[row].id_payment)
            self.paymentController.purchase_payment(test_data[row].id_payment, amount, price)
            self.populate_table()
            QMessageBox.information(self, "Успіх", "Матеріал докуплено успішно.")
        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Сталася помилка: {e}")

    def process_remove(self, matherial_id):
        # Обробка даних докупівлі
        try:
            reply = QMessageBox.question(self, "Підтвердження видалення",
                                         "Ви впевнені, що хочете видалити матеріал?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                if self.table_as == "planned":
                    self.matherialController.remove_matherial(matherial_id)
                    self.populate_table()
                    QMessageBox.information(self, "Успіх", "Матеріал успішно видалено.")
                elif self.table_as == "history":
                    self.historyController.remove_history(matherial_id)
                    self.populate_table()
                    QMessageBox.information(self, "Успіх", "Матеріал успішно видалено.")
                elif self.table_as == "payment":
                    self.paymentController.remove_matherial(matherial_id)
                    self.populate_table()
                    QMessageBox.information(self, "Успіх", "Матеріал успішно видалено.")

        except Exception as e:
            QMessageBox.critical(self, "Помилка", f"Сталася помилка: {e}")

    def populate_table(self):
        # Відключаємо сигнал перед заповненням таблиці
        self.updating_table = True
        self.table.blockSignals(True)

        # Завантаження даних з бази даних
        if self.table_as == "planned":
            test_data = None
            if self.stage:
                test_data = self.matherialController.view_matherial(self.stage.id_stages)
            elif self.sub_stage:
                test_data = self.matherialController.view_matherial(None,self.sub_stage.id_sub_stage)
            summa = 0
            for row_index, material in enumerate(test_data):
                summa += material.sum
            self.setWindowTitle(self.table_as + " Загальна Сумма: " + str(summa))
            self.table.clear()
            self.table.setColumnCount(6)
            self.table.setHorizontalHeaderLabels(["Назва матеріалу", "од. вимір.", "Кількість", "Ціна", "Сумма", "Дія"])
            self.table.setRowCount(len(test_data) + 1)
            try:
                for row_index, material in enumerate(test_data):
                    button = QPushButton("Видалити")
                    button.clicked.connect(lambda _, r=row_index: self.process_remove(test_data[r].id_matherial))
                    # Отримуємо дані з об'єкта Matherial
                    row_data = [
                        material.matherial_name,
                        material.unit,
                        material.amount,
                        material.price,
                        material.sum,
                        button
                    ]

                    for col_index, item in enumerate(row_data):
                        if col_index != 5:
                            self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))
                        else:
                            self.table.setCellWidget(row_index, 5, button)
            except Exception as e:
                print("Error Data View:", e)
        elif self.table_as == "purchased":
            if self.stage:
                test_data = self.matherialPurchController.view_matherial(self.stage.id_stages)
            else:
                test_data = self.matherialPurchController.view_matherial(None, self.sub_stage.id_sub_stage)


            self.table.setColumnCount(7)
            self.table.setHorizontalHeaderLabels(["Назва матеріалу", "од. вимір.", "Кількість", "Ціна", "Сумма", "Дія", "Історія"])
            summa = 0
            for row_index, material in enumerate(test_data):
                summa += material.sum
            self.setWindowTitle(self.table_as + " Загальна Сумма: " + str(summa))
            self.table.setRowCount(len(test_data) + 1)
            try:
                for row_index, material in enumerate(test_data):
                    button_purch = QPushButton("Докупити")
                    button_purch.clicked.connect(lambda _, r=row_index: self.open_purchase_dialog(r,test_data))
                    button_history = QPushButton("Історія")
                    button_history.clicked.connect(lambda _, r=row_index: self.showHistoryTable(test_data[r].id_matherial))
                    # Отримуємо дані з об'єкта Matherial
                    row_data = [
                        material.matherial_name,
                        material.unit,
                        material.amount,
                        material.price,
                        material.sum,
                        button_purch,
                        button_history
                    ]

                    for col_index, item in enumerate(row_data):
                        if col_index < 5:
                            self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))
                        elif col_index == 5:
                            self.table.setCellWidget(row_index, 5, button_purch)
                        elif col_index == 6:
                            self.table.setCellWidget(row_index, 6, button_history)
            except Exception as e:
                print("Error Data View:", e)
        elif self.table_as == "payment":
            if self.stage:
                test_data_pay = self.paymentController.view_payment(self.stage.id_stages)
            else:
                test_data_pay = self.paymentController.view_payment(None, self.sub_stage.id_sub_stage)
            self.table.clear()
            self.table.setColumnCount(8)
            self.table.setHorizontalHeaderLabels(
                ["Назва матеріалу", "од. вимір.", "Кількість", "Ціна", "Сумма", "Дія", "Історія", "Видалення"])
            summa = 0
            for row_index, payment in enumerate(test_data_pay):
                summa += payment.sum
            self.setWindowTitle(self.table_as + " Загальна Сумма: " + str(summa))
            self.table.setRowCount(len(test_data_pay) + 1)
            try:
                for row_index, payment in enumerate(test_data_pay):
                    button_pay = QPushButton("Доплатити")
                    button_pay.clicked.connect(lambda _, r=row_index: self.open_payment_dialog(r,test_data_pay))
                    button_history = QPushButton("Історія")
                    button_history.clicked.connect(lambda _, r=row_index: self.showHistoryTable(None, test_data_pay[r].id_payment))
                    button_delete = QPushButton("Видалити")
                    button_delete.clicked.connect(lambda _, r=row_index: self.process_remove(test_data_pay[r].id_payment))
                    # Отримуємо дані з об'єкта Matherial
                    row_data = [
                        payment.matherial_name,
                        payment.unit,
                        payment.amount,
                        payment.price,
                        payment.sum,
                        button_pay,
                        button_history,
                        button_delete
                    ]

                    for col_index, item in enumerate(row_data):
                        if col_index < 5:
                            self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))
                        elif col_index == 5:
                            self.table.setCellWidget(row_index, 5, button_pay)
                        elif col_index == 6:
                            self.table.setCellWidget(row_index, 6, button_history)
                        elif col_index == 7:
                            self.table.setCellWidget(row_index, 7, button_delete)
            except Exception as e:
                print("Error Data View:", e)
        elif self.table_as == "history":
            if self.matheriales_id:
                test_data_history = self.historyController.view_history(self.matheriales_id)
            else:
                test_data_history = self.historyController.view_history(None, self.paymentes_id)
            self.table.setColumnCount(6)
            summa = 0
            for row_index, history in enumerate(test_data_history):
                summa += history.sum
            self.setWindowTitle(self.table_as + " Загальна Сумма: " + str(summa))
            self.table.clear()
            if self.matheriales_id:
                self.table.setHorizontalHeaderLabels(["Дата та час", "Постачальник", "Кількість", "Ціна", "Сумма", "Дія"])
            else:
                self.table.setHorizontalHeaderLabels(["Дата та час", "Працівник", "Кількість", "Ціна", "Сумма", "Дія"])
            self.table.setRowCount(len(test_data_history))
            try:
                for row_index, history in enumerate(test_data_history):
                    button = QPushButton("Видалити")
                    button.clicked.connect(lambda _, r=row_index: self.process_remove(test_data_history[r].id_history))
                    # Отримуємо дані з об'єкта Matherial
                    row_data = [
                        history.time_buy,
                        history.provider,
                        history.amount,
                        history.price,
                        history.sum,
                        button
                    ]

                    for col_index, item in enumerate(row_data):
                        if col_index != 5:
                            self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))
                        else:
                            self.table.setCellWidget(row_index, 5, button)

            except Exception as e:
                print("Error Data View:", e)
        else:
            if self.stage:
                test_data_planned = self.matherialController.view_matherial(self.stage.id_stages)
                test_data_purchaced = self.matherialPurchController.view_matherial(self.stage.id_stages)
            else:
                test_data_planned = self.matherialController.view_matherial(None, self.sub_stage.id_sub_stage)
                test_data_purchaced = self.matherialPurchController.view_matherial(None, self.sub_stage.id_sub_stage)
            summa = 0
            self.table.setColumnCount(5)
            self.table.setRowCount(len(test_data_planned))
            try:
                for row_index, material in enumerate(test_data_planned):
                    # Отримуємо дані з об'єкта Matherial
                    row_data = [
                        material.matherial_name,
                        material.unit,
                        material.amount - test_data_purchaced[row_index].amount,
                        test_data_purchaced[row_index].price,
                        material.sum - test_data_purchaced[row_index].sum
                    ]
                    summa += material.sum - test_data_purchaced[row_index].sum

                    self.setWindowTitle(self.table_as + " Загальна Сумма: " + str(summa))
                    for col_index, item in enumerate(row_data):
                        self.table.setItem(row_index, col_index, QTableWidgetItem(str(item)))
            except Exception as e:
                print("Error Data View:", e)

        # Підключаємо сигнал після заповнення таблиці
        self.table.blockSignals(False)
        self.updating_table = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MaterialView()
    window.show()
    sys.exit(app.exec_())
