import json

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PySide6.QtWidgets import QGraphicsOpacityEffect, QWidget

from app.ui.map_search_overlay import MapSearchOverlay
from app.ui.map_view import MapView


class MapWithSearchOverlay(QWidget):
    """Full-bleed map with a top-centered floating search bar (auto-hide UX)."""

    ZOOM_HIDE_THRESHOLD = 9

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._map = MapView(self)
        self._search = MapSearchOverlay(self)
        self._search.raise_()

        self._search_fx = QGraphicsOpacityEffect(self._search)
        self._search.setGraphicsEffect(self._search_fx)
        self._search_fx.setOpacity(1.0)

        self._search_anim: QPropertyAnimation | None = None

        self._ux_zoom = 6
        self._ux_suppress = False
        self._ux_force_show = False
        self._last_marker_t = 0
        self._last_empty_t = 0
        self._search_bar_visible = True

        self._map.ux_snapshot_ready.connect(self._on_map_ux_json)
        self._search.book_chosen.connect(self._on_book_chosen_from_search)
        self._search.book_chosen.connect(self._map.fly_to_book)

    @property
    def map_view(self) -> MapView:
        return self._map

    @property
    def search_overlay(self) -> MapSearchOverlay:
        return self._search

    def apply_language(self, locale: str) -> None:
        self._search.apply_language(locale)

    def set_entries(self, entries: list[dict], locale: str = "tr") -> None:
        self._map.set_entries(entries, locale)
        self._search.set_entries(entries)
        self.apply_language(locale)

    def _on_book_chosen_from_search(self, _book_id: int) -> None:
        self._ux_suppress = True
        self._ux_force_show = False
        self._recompute_search_bar()

    def _on_map_ux_json(self, payload: str) -> None:
        if not payload:
            return
        try:
            d = json.loads(payload)
        except json.JSONDecodeError:
            return
        z = int(d.get("z", self._ux_zoom))
        marker_t = int(d.get("markerT", 0))
        empty_t = int(d.get("emptyT", 0))

        self._ux_zoom = z
        if z <= self.ZOOM_HIDE_THRESHOLD:
            self._ux_suppress = False

        if marker_t > self._last_marker_t:
            self._last_marker_t = marker_t
            self._ux_suppress = True
            self._ux_force_show = False

        if empty_t > self._last_empty_t:
            self._last_empty_t = empty_t
            self._ux_force_show = True
            self._ux_suppress = False

        self._recompute_search_bar()

    def _recompute_search_bar(self) -> None:
        z = self._ux_zoom
        visible = self._ux_force_show or (z <= self.ZOOM_HIDE_THRESHOLD and not self._ux_suppress)
        if visible == self._search_bar_visible:
            return
        self._search_bar_visible = visible
        self._animate_search_bar(visible)

    def _animate_search_bar(self, visible: bool) -> None:
        target = 1.0 if visible else 0.0
        if visible:
            self._search.setAttribute(Qt.WidgetAttribute.WA_TransparentForInput, False)
        if self._search_anim is not None:
            self._search_anim.stop()
        self._search_anim = QPropertyAnimation(self._search_fx, b"opacity", self)
        self._search_anim.setDuration(200)
        self._search_anim.setStartValue(self._search_fx.opacity())
        self._search_anim.setEndValue(target)
        self._search_anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        def _finished() -> None:
            self._search.setAttribute(Qt.WidgetAttribute.WA_TransparentForInput, not visible)
            self._search_anim = None

        self._search_anim.finished.connect(_finished)
        self._search_anim.start()

    def relayout_search(self) -> None:
        self._search.adjustSize()
        margin_x = 16
        top = 14
        max_w = min(520, max(280, self.width() - 2 * margin_x))
        h = max(self._search.sizeHint().height(), self._search.minimumSizeHint().height())
        self._search.setGeometry((self.width() - max_w) // 2, top, max_w, h)

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._map.setGeometry(self.rect())
        self.relayout_search()
        self._search.raise_()
