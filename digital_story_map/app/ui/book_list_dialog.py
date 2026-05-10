from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from app.i18n import t
from app.ui.search_utils import entry_city


class BookListDialog(QDialog):
    """Scrollable full catalog; double-click flies to selection."""

    book_selected = Signal(int)

    def __init__(self, entries: list[dict], parent=None, locale: str = "tr") -> None:
        super().__init__(parent)
        self._locale = locale if locale in ("tr", "en") else "tr"
        self.setWindowTitle(t(self._locale, "book_list_window"))
        self.resize(520, 640)
        self.setModal(True)

        self._title = QLabel()
        self._title.setObjectName("bookListTitle")

        self._hint = QLabel()
        self._hint.setObjectName("aboutSub")
        self._hint.setWordWrap(True)

        self._list = QListWidget()
        self._list.setAlternatingRowColors(True)
        sorted_entries = sorted(entries, key=lambda e: str(e.get("title", "")).lower())
        for e in sorted_entries:
            city = entry_city(e)
            line = f"{e.get('title', '')} — {e.get('author', '')}"
            if city:
                line += f" ({city})"
            it = QListWidgetItem(line)
            it.setData(Qt.ItemDataRole.UserRole, int(e.get("id", 0)))
            self._list.addItem(it)

        self._list.itemDoubleClicked.connect(self._emit_and_close)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self._title)
        layout.addWidget(self._hint)
        layout.addWidget(self._list, stretch=1)
        layout.addWidget(buttons)

        self._apply_texts()

    def _apply_texts(self) -> None:
        self.setWindowTitle(t(self._locale, "book_list_window"))
        self._title.setText(t(self._locale, "book_list_title"))
        self._hint.setText(t(self._locale, "book_list_hint"))
