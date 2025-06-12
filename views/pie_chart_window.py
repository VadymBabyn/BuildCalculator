from PyQt5.QtWidgets import (
    QVBoxLayout, QPushButton, QApplication, QDialog, QComboBox, QLabel, QFileDialog, QSizePolicy
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from utils.pytorch_model import CostPredictionService


class PieChartWindow(QDialog):
    def __init__(self, data):
        super().__init__()
        self.setWindowTitle("Аналіз витрат")
        self.setGeometry(100, 100, 1000, 600)
        self.data = [d for d in data if d["planned"] > 0 or d["actual"] > 0]
        self.predictor = CostPredictionService()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Комбобокс для вибору типу графіку
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Кругова", "Стовпчикова"])
        self.chart_type.currentIndexChanged.connect(self.plot)
        layout.addWidget(self.chart_type)

        # Кнопка збереження
        save_btn = QPushButton("Зберегти у PNG")
        save_btn.clicked.connect(self.save_chart)
        layout.addWidget(save_btn)

        # Площина для графіків
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.canvas)

        # Місце для виводу аналізу
        self.analysis_label = QLabel()
        self.analysis_label.setWordWrap(True)
        layout.addWidget(self.analysis_label)

        self.plot()

    def analyze_and_predict(self, stages):
        # Прогнозована модель вже обробить занижені actual
        total_planned = sum(s["planned"] for s in stages)
        total_actual = sum(s["actual"] for s in stages)

        diff = total_actual - total_planned

        analysis_text = (
            f"<b>Загальна сума:</b><br>"
            f"▸ Заплановано: {total_planned:,} грн<br>"
            f"▸ Фактично (наявні): {total_actual:,} грн<br>"
        )

        if diff > 0:
            analysis_text += f"<span style='color:red;'>➤ Бюджет перевищено на {diff:,} грн</span><br>"
        elif diff < 0:
            analysis_text += f"<span style='color:green;'>➤ Економія: {-diff:,} грн</span><br>"
        else:
            analysis_text += "<span style='color:blue;'>➤ Витрати точно по плану</span><br>"

        # Прогнозування загальної фактичної вартості
        predicted_total = self.predictor.train_and_predict(stages)
        if predicted_total:
            analysis_text += (
                f"<br><b>Прогнозована загальна вартість:</b><br>"
                f"🔮 {predicted_total:,} грн<br>"
                f"📉 Очікуване відхилення: {predicted_total - total_planned:,} грн"
            )
        else:
            analysis_text += (
                "<br><i>Недостатньо даних для прогнозу: потрібно більше 3 етапів з наявними фактичними даними.</i>"
            )

        self.analysis_label.setText(analysis_text)
        self.canvas.draw()

    def plot(self):
        self.figure.clear()
        chart_type = self.chart_type.currentText()
        if chart_type == "Стовпчикова":
            ax1 = self.figure.add_subplot(111)
            ax2 = None
        else:
            ax1 = self.figure.add_subplot(121)
            ax2 = self.figure.add_subplot(122)

        labels = [d["stage"] for d in self.data]
        planned = [d["planned"] for d in self.data]
        actual = [d["actual"] for d in self.data]

        def make_autopct(values):
            def my_autopct(pct):
                total = sum(values)
                val = int(round(pct * total / 100.0))
                return f'{pct:.1f}%\n({val} грн)'
            return my_autopct

        # Pie charts
        if chart_type == "Кругова":
            from matplotlib import cm
            color_map = cm.get_cmap('tab20', len(labels))
            colors = [color_map(i) for i in range(len(labels))]

            planned_labels = [f"{label} ({value:,} грн)" for label, value in zip(labels, planned)]
            actual_labels = [f"{label} ({value:,} грн)" for label, value in zip(labels, actual)]

            def autopct_filter(pct):
                return f"{pct:.1f}%" if pct >= 3 else ""

            wedges1, texts1, autotexts1 = ax1.pie(
                planned,
                labels=None,
                autopct=autopct_filter,
                startangle=140,
                colors=colors
            )
            ax1.legend(wedges1, planned_labels, title="Етапи", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            ax1.set_title("Заплановані витрати")

            wedges2, texts2, autotexts2 = ax2.pie(
                actual,
                labels=None,
                autopct=autopct_filter,
                startangle=140,
                colors=colors
            )
            ax2.legend(wedges2, actual_labels, title="Етапи", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            ax2.set_title("Фактичні витрати")


        elif chart_type == "Стовпчикова":
            x = range(len(labels))
            bar_width = 0.35

            bars1 = ax1.bar(x, planned, width=bar_width, label='Заплановано', color='skyblue')
            bars2 = ax1.bar([p + bar_width for p in x], actual, width=bar_width, label='Фактично', color='orange')

            ax1.set_xticks([p + bar_width / 2 for p in x])
            ax1.set_xticklabels(labels, rotation=45, ha="right")
            ax1.set_title("Порівняння витрат по етапах")
            ax1.legend()

            # Підписи на стовпцях
            for bar in bars1:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2, height + 200, f'{int(height)}', ha='center', va='bottom', rotation=90)

            for bar in bars2:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width() / 2, height + 200, f'{int(height)}', ha='center', va='bottom', rotation=90)

            if ax2 in self.figure.axes:
                self.figure.delaxes(ax2)

        self.analyze_and_predict(self.data)
        self.canvas.draw()

    def save_chart(self):
        chart_type = self.chart_type.currentText().replace(" ", "_").lower()
        default_filename = f"stage_detail_{chart_type}.png"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Зберегти діаграму як PNG",
            default_filename,
            "PNG файли (*.png);;Всі файли (*)"
        )

        if file_path:
            self.figure.savefig(file_path)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = PieChartWindow(data=[])
    window.show()

    sys.exit(app.exec_())