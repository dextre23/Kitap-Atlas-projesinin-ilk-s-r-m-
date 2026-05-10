from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout

from app.i18n import t


class AboutDialog(QDialog):
    def __init__(self, parent=None, locale: str = "tr") -> None:
        super().__init__(parent)
        self._locale = locale if locale in ("tr", "en") else "tr"
        self.resize(440, 320)
        self.setModal(True)

        self._head = QLabel()
        self._head.setObjectName("aboutHead")

        self._sub = QLabel()
        self._sub.setObjectName("aboutSub")

        self._body = QLabel()
        self._body.setObjectName("aboutBody")
        self._body.setTextFormat(Qt.TextFormat.RichText)
        self._body.setWordWrap(True)
        self._body.setAlignment(Qt.AlignmentFlag.AlignTop)

        self._close_btn = QPushButton()
        self._close_btn.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.addWidget(self._head)
        layout.addWidget(self._sub)
        layout.addWidget(self._body, stretch=1)
        layout.addWidget(self._close_btn, alignment=Qt.AlignmentFlag.AlignRight)

        self._apply_texts()

    def _apply_texts(self) -> None:
        self.setWindowTitle(t(self._locale, "about_window"))
        self._head.setText(t(self._locale, "about_head"))
        self._sub.setText(t(self._locale, "about_sub"))
        self._body.setText(str(t(self._locale, "about_body")))
        self._close_btn.setText(t(self._locale, "close"))
