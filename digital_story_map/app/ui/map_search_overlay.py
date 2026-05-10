from PySide6.QtCore import QTimer, Qt, Signal
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.i18n import t
from app.ui.search_utils import entry_city, filter_entries_for_suggest


class MapSearchOverlay(QWidget):
    """Top-centered glass-style search with title-focused suggestions (filtered by title, author, city)."""

    book_chosen = Signal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._entries: list[dict] = []
        self._locale: str = "tr"
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        glass = QFrame()
        glass.setObjectName("mapSearchGlass")

        self._input = QLineEdit()
        self._input.setObjectName("mapSearchInput")
        self._input.textChanged.connect(self._on_text)
        self._input.returnPressed.connect(self._pick_first_suggestion)

        self._hint = QLabel()
        self._hint.setObjectName("mapSearchHint")

        self._list = QListWidget()
        self._list.setObjectName("mapSearchSuggestList")
        self._list.setMaximumHeight(260)
        self._list.hide()
        self._list.itemClicked.connect(self._on_suggest_clicked)

        inner = QVBoxLayout(glass)
        inner.setContentsMargins(14, 12, 14, 12)
        inner.setSpacing(8)
        inner.addWidget(self._input)
        inner.addWidget(self._hint)
        inner.addWidget(self._list)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.addWidget(glass)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._maybe_hide_list)
        self._input.installEventFilter(self)
        self.apply_language(self._locale)

    def apply_language(self, locale: str) -> None:
        self._locale = locale if locale in ("tr", "en") else "tr"
        self._input.setPlaceholderText(t(self._locale, "search_placeholder"))
        self._hint.setText(t(self._locale, "search_hint"))

    def set_entries(self, entries: list[dict]) -> None:
        self._entries = entries

    def _on_text(self, text: str) -> None:
        self._list.clear()
        matches = filter_entries_for_suggest(self._entries, text, limit=14)
        if not text.strip() or not matches:
            self._list.hide()
            self._relayout_parent()
            return
        for e in matches:
            city = entry_city(e)
            line = f"{e.get('title', '')}  —  {e.get('author', '')}"
            if city:
                line += f"  ·  {city}"
            it = QListWidgetItem(line)
            it.setData(Qt.ItemDataRole.UserRole, int(e.get("id", 0)))
            self._list.addItem(it)
        self._list.show()
        self._relayout_parent()

    def _relayout_parent(self) -> None:
        self.adjustSize()
        parent = self.parent()
        if parent is not None and hasattr(parent, "relayout_search"):
            parent.relayout_search()

    def _pick_first_suggestion(self) -> None:
        if self._list.count() > 0:
            item = self._list.item(0)
            self._activate_item(item)

    def _on_suggest_clicked(self, item: QListWidgetItem) -> None:
        self._activate_item(item)

    def _activate_item(self, item: QListWidgetItem | None) -> None:
        if item is None:
            return
        bid = item.data(Qt.ItemDataRole.UserRole)
        if isinstance(bid, int) and bid > 0:
            self._input.clear()
            self._list.hide()
            self._list.clear()
            self.book_chosen.emit(bid)
            self._relayout_parent()

    def eventFilter(self, obj, event) -> bool:
        if obj is self._input and event.type() == event.Type.FocusOut:
            self._hide_timer.start(200)
        elif obj is self._input and event.type() == event.Type.FocusIn:
            self._hide_timer.stop()
        return super().eventFilter(obj, event)

    def _maybe_hide_list(self) -> None:
        app = QApplication.instance()
        fw = app.focusWidget() if app else None
        if fw is self._input or fw is self._list:
            return
        if fw is not None and (self.isAncestorOf(fw) or self._list.isAncestorOf(fw)):
            return
        self._list.hide()
        self._relayout_parent()
