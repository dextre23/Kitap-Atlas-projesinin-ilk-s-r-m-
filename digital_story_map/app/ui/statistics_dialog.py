from collections import Counter

from PySide6.QtCharts import QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QValueAxis
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtWidgets import QDialog, QVBoxLayout

from app.i18n import t
from app.ui.search_utils import entry_city


class StatisticsDialog(QDialog):
    def __init__(self, entries: list[dict], parent=None, locale: str = "tr") -> None:
        super().__init__(parent)
        self._locale = locale if locale in ("tr", "en") else "tr"
        self.setWindowTitle(t(self._locale, "stats_window"))
        self.resize(760, 460)

        layout = QVBoxLayout(self)
        chart_view = QChartView(self._build_city_chart(entries))
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        layout.addWidget(chart_view)

    def _build_city_chart(self, entries: list[dict]) -> QChart:
        city_counts = Counter()
        for item in entries:
            city = entry_city(item)
            if city:
                city_counts[city] += 1

        top = city_counts.most_common(5)
        categories = [city for city, _ in top] or [str(t(self._locale, "chart_no_data"))]
        values = [count for _, count in top] or [0]

        bar_set = QBarSet(str(t(self._locale, "chart_books")))
        bar_set.append(values)

        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(str(t(self._locale, "chart_top_cities")))
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        chart.setBackgroundVisible(False)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_y = QValueAxis()
        axis_y.setLabelFormat("%d")
        axis_y.setTitleText(str(t(self._locale, "chart_count")))

        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_x)
        series.attachAxis(axis_y)
        return chart
