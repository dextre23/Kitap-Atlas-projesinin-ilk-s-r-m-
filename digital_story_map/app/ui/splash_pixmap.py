"""Programmatic splash artwork (Turkish landscape motif) with no external image."""

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPainterPath, QPen, QPixmap


def create_splash_pixmap(width: int = 900, height: int = 520) -> QPixmap:
    pm = QPixmap(width, height)
    pm.fill(QColor("#0a0e14"))

    painter = QPainter(pm)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    sky = QLinearGradient(0, 0, 0, height * 0.62)
    sky.setColorAt(0.0, QColor("#1a2a4a"))
    sky.setColorAt(0.45, QColor("#2d4a7c"))
    sky.setColorAt(1.0, QColor("#4a6fa8"))
    painter.fillRect(QRectF(0, 0, width, height * 0.62), sky)

    horizon_y = height * 0.58
    land = QLinearGradient(0, horizon_y, 0, height)
    land.setColorAt(0.0, QColor("#1e2d22"))
    land.setColorAt(1.0, QColor("#0f1610"))
    painter.fillRect(QRectF(0, horizon_y, width, height - horizon_y), land)

    sun_pen = QPen(QColor("#f4d03f"))
    sun_pen.setWidth(2)
    painter.setPen(sun_pen)
    painter.setBrush(QColor("#f4d03f33"))
    painter.drawEllipse(QPointF(width * 0.78, height * 0.22), 38, 38)

    hills = QPainterPath()
    hills.moveTo(0, horizon_y + 8)
    hills.cubicTo(
        width * 0.2,
        horizon_y - 40,
        width * 0.35,
        horizon_y + 30,
        width * 0.5,
        horizon_y - 10,
    )
    hills.cubicTo(
        width * 0.65,
        horizon_y - 50,
        width * 0.82,
        horizon_y + 20,
        width,
        horizon_y - 5,
    )
    hills.lineTo(width, height)
    hills.lineTo(0, height)
    hills.closeSubpath()
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#243028"))
    painter.drawPath(hills)

    painter.setPen(QColor("#e8ebf2"))
    painter.setFont(painter.font())
    f = painter.font()
    f.setPointSize(26)
    f.setBold(True)
    painter.setFont(f)
    painter.drawText(QRectF(40, height * 0.12, width - 80, 50), Qt.AlignmentFlag.AlignLeft, "Kitap Atlası")

    f.setPointSize(12)
    f.setBold(False)
    painter.setFont(f)
    painter.setPen(QColor("#b8c4d9"))
    painter.drawText(
        QRectF(40, height * 0.12 + 44, width - 80, 40),
        Qt.AlignmentFlag.AlignLeft,
        "Turkish literature · spatial narratives · 1980+",
    )

    painter.end()
    return pm
