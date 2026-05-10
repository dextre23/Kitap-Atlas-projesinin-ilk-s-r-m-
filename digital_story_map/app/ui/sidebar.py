from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from app.i18n import t


class SidebarWidget(QWidget):
    book_catalog_requested = Signal()
    about_requested = Signal()
    stats_requested = Signal()
    locale_changed = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("sidebarRoot")
        self.setMinimumWidth(260)
        self.setMaximumWidth(320)

        self._locale = "tr"

        self._title = QLabel()
        self._title.setObjectName("sidebarTitle")

        self._tag = QLabel()
        self._tag.setObjectName("sidebarTag")
        self._tag.setWordWrap(True)

        locale_bar = QWidget()
        locale_bar.setObjectName("localeBar")
        loc_layout = QHBoxLayout(locale_bar)
        loc_layout.setContentsMargins(0, 0, 0, 0)
        loc_layout.setSpacing(6)

        self._loc_label = QLabel()
        self._loc_label.setObjectName("localeLabel")

        self._btn_tr = QPushButton("TR")
        self._btn_en = QPushButton("EN")
        for b in (self._btn_tr, self._btn_en):
            b.setObjectName("localePill")
            b.setCheckable(True)
            b.setAutoExclusive(False)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
        self._btn_tr.setChecked(True)
        self._btn_tr.clicked.connect(lambda: self._apply_locale("tr"))
        self._btn_en.clicked.connect(lambda: self._apply_locale("en"))

        loc_layout.addWidget(self._loc_label)
        loc_layout.addWidget(self._btn_tr, stretch=1)
        loc_layout.addWidget(self._btn_en, stretch=1)

        self.btn_books = QPushButton()
        self.btn_books.setObjectName("sidebarPrimaryBtn")
        self.btn_books.clicked.connect(self.book_catalog_requested.emit)

        self.btn_stats = QPushButton()
        self.btn_stats.clicked.connect(self.stats_requested.emit)

        self.btn_about = QPushButton()
        self.btn_about.setObjectName("sidebarGhostBtn")
        self.btn_about.clicked.connect(self.about_requested.emit)

        self._footer = QLabel()
        self._footer.setObjectName("sidebarFooter")
        self._footer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 24, 20, 20)
        layout.setSpacing(12)
        layout.addWidget(self._title)
        layout.addWidget(self._tag)
        layout.addWidget(locale_bar)
        layout.addSpacing(8)
        layout.addWidget(self.btn_books)
        layout.addWidget(self.btn_stats)
        layout.addWidget(self.btn_about)
        layout.addStretch(1)
        layout.addWidget(self._footer)

        self.apply_language(self._locale)

    def apply_language(self, locale: str) -> None:
        self._locale = locale if locale in ("tr", "en") else "tr"
        self._title.setText(t(self._locale, "app_title"))
        self._tag.setText(t(self._locale, "sidebar_tag"))
        self._loc_label.setText(t(self._locale, "lang_label"))
        self.btn_books.setText(t(self._locale, "btn_books"))
        self.btn_stats.setText(t(self._locale, "btn_stats"))
        self.btn_about.setText(t(self._locale, "btn_about"))
        self._footer.setText(t(self._locale, "footer"))

    def _apply_locale(self, code: str) -> None:
        self._btn_tr.setChecked(code == "tr")
        self._btn_en.setChecked(code == "en")
        self.apply_language(code)
        self.locale_changed.emit(code)
