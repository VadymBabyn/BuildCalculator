from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QApplication, QDialog, QComboBox, QLabel, QHBoxLayout, QFileDialog
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class SingleStageDetailChartWindow(QDialog):
    def __init__(self, stage_data):
        super().__init__()
        self.setWindowTitle("Деталізація витрат по етапу")
        self.setGeometry(200, 150, 1200, 700)
        self.stage_data = stage_data

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Ряд для вибору типу діаграми і типу даних
        selector_layout = QHBoxLayout()

        # Комбобокс для типу даних
        self.chart_selector = QComboBox()
        self.chart_selector.addItems([
            "Матеріали - Заплановано",
            "Матеріали - Фактично",
            "Послуги"
        ])
        self.chart_selector.currentIndexChanged.connect(self.plot)
        selector_layout.addWidget(QLabel("Тип даних:"))
        selector_layout.addWidget(self.chart_selector)

        # Комбобокс для типу діаграми
        self.chart_type_selector = QComboBox()
        self.chart_type_selector.addItems([
            "Кругова", "Стовпчикова"
        ])
        self.chart_type_selector.currentIndexChanged.connect(self.plot)
        selector_layout.addWidget(QLabel("Тип діаграми:"))
        selector_layout.addWidget(self.chart_type_selector)

        layout.addLayout(selector_layout)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти діаграму як PNG")
        save_btn.clicked.connect(self.save_chart)
        layout.addWidget(save_btn)

        # Графік
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot()

    def plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        data_type = self.chart_selector.currentText()
        chart_type = self.chart_type_selector.currentText()

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f'{pct:.1f}%\n({val} грн)'
            return my_autopct

        labels, values, title = [], [], ""

        if data_type == "Матеріали - Заплановано":
            items = [m for m in self.stage_data.get("materials", []) if m["planned"] > 0]
            labels = [m["name"] for m in items]
            values = [m["planned"] for m in items]
            title = "Заплановані витрати на матеріали"

        elif data_type == "Матеріали - Фактично":
            items = [m for m in self.stage_data.get("materials", []) if m["actual"] > 0]
            labels = [m["name"] for m in items]
            values = [m["actual"] for m in items]
            title = "Фактичні витрати на матеріали"

        elif data_type == "Послуги":
            items = [s for s in self.stage_data.get("services", []) if s["amount"] > 0]
            labels = [s["name"] for s in items]
            values = [s["amount"] for s in items]
            title = "Витрати на послуги"

        # Побудова діаграми
        if chart_type == "Кругова":
            ax.pie(values, labels=labels, autopct=make_autopct(values), startangle=140)
        else:  # Стовпчикова
            bars = ax.bar(labels, values, color='skyblue')
            ax.set_ylabel("Сума (грн)")
            ax.set_xticklabels(labels, rotation=45, ha='right')
            ax.set_ylim(0, max(values) * 1.2)
            # Додати підписи над стовпчиками
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f'{value} грн',
                    ha='center',
                    va='bottom',
                    fontsize=9,
                    rotation=0
                )

        ax.set_title(title)
        self.canvas.draw()

    def save_chart(self):
        chart_type = self.chart_selector.currentText().replace(" ", "_").lower()
        default_filename = f"stage_detail_{chart_type}.png"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Зберегти діаграму як PNG",
            default_filename,
            "PNG файли (*.png);;Всі файли (*)"
        )

        if file_path:
            self.figure.savefig(file_path)

# Тест
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = SingleStageDetailChartWindow(stage_data=[])
    win.show()
    sys.exit(app.exec_())
