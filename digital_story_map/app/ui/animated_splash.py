"""Frameless animated splash: undulating sine wave, sun, loading text."""

from __future__ import annotations

import math

from PySide6.QtCore import QPointF, QRectF, Qt, QTimer
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QWidget


class AnimatedSplashScreen(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(
            parent,
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.SplashScreen,
        )
        self._phase = 0.0
        self.setFixedSize(900, 520)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._tick)
        self._timer.start(16)

    def _tick(self) -> None:
        self._phase += 0.045
        self.update()

    def paintEvent(self, event) -> None:
        w, h = float(self.width()), float(self.height())
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        sky = QLinearGradient(0, 0, 0, h * 0.62)
        sky.setColorAt(0.0, QColor("#141e35"))
        sky.setColorAt(0.5, QColor("#243a64"))
        sky.setColorAt(1.0, QColor("#4a6fa8"))
        p.fillRect(self.rect(), sky)

        horizon = h * 0.58
        land_grad = QLinearGradient(0, horizon, 0, h)
        land_grad.setColorAt(0.0, QColor("#1a2620"))
        land_grad.setColorAt(1.0, QColor("#0c100c"))
        p.fillRect(QRectF(0, horizon, w, h - horizon), land_grad)

        p.setPen(QPen(QColor("#f4d03f"), 2))
        p.setBrush(QColor("#f4d03f44"))
        p.drawEllipse(QPointF(w * 0.78, h * 0.2), 36, 36)

        title_font = QFont("Segoe UI", 26, QFont.Weight.Bold)
        p.setFont(title_font)
        p.setPen(QColor("#f0f3f8"))
        p.drawText(QRectF(40, h * 0.1, w - 80, 48), Qt.AlignmentFlag.AlignLeft, "Kitap Atlası")

        sub_font = QFont("Segoe UI", 12)
        p.setFont(sub_font)
        p.setPen(QColor("#b8c4d9"))
        p.drawText(QRectF(40, h * 0.1 + 42, w - 80, 32), Qt.AlignmentFlag.AlignLeft, "Kitap Atlası yükleniyor...")

        wave_path = QPainterPath()
        base_y = h * 0.72
        steps = 56
        points: list[tuple[float, float]] = []
        for i in range(steps + 1):
            x = (i / steps) * w
            ang = (x / w) * math.tau * 2.2 + self._phase
            y = base_y + math.sin(ang) * 14 + math.sin(ang * 0.5 + 1.1) * 6
            points.append((x, y))
        wave_path.moveTo(0, h)
        wave_path.lineTo(0, points[0][1])
        for x, y in points:
            wave_path.lineTo(x, y)
        wave_path.lineTo(w, h)
        wave_path.closeSubpath()
        p.setPen(Qt.PenStyle.NoPen)
        p.setBrush(QColor("#1e2d28"))
        p.drawPath(wave_path)

        wave_path2 = QPainterPath()
        base_y2 = h * 0.78
        pts2: list[tuple[float, float]] = []
        for i in range(steps + 1):
            x = (i / steps) * w
            ang = (x / w) * math.tau * 2.8 - self._phase * 1.1
            y = base_y2 + math.sin(ang) * 10
            pts2.append((x, y))
        wave_path2.moveTo(0, h)
        wave_path2.lineTo(0, pts2[0][1])
        for x, y in pts2:
            wave_path2.lineTo(x, y)
        wave_path2.lineTo(w, h)
        wave_path2.closeSubpath()
        p.setBrush(QColor("#152018"))
        p.drawPath(wave_path2)

        p.end()
