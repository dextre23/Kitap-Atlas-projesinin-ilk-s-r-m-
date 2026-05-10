from PySide6.QtCore import QUrl, Signal, QTimer
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

from app.services.map_http_server import MapHttpServer
from app.services.map_service import build_map_html


class MapView(QWebEngineView):
    """Emits JSON snapshot string from window.__kitapUx for search-bar UX (poll)."""

    ux_snapshot_ready = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._entries: list[dict] = []
        self._locale: str = "tr"
        self._server = MapHttpServer.instance()
        self._server.ensure_running()

        s = self.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)

        self._poll = QTimer(self)
        self._poll.setInterval(110)
        self._poll.timeout.connect(self._poll_ux_snapshot)
        self.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok: bool) -> None:
        if ok and not self._poll.isActive():
            self._poll.start()

    def _poll_ux_snapshot(self) -> None:
        self.page().runJavaScript(
            "(function(){ try { return JSON.stringify(window.__kitapUx || {}); } catch (e) { return \"{}\"; } })()",
            self.ux_snapshot_ready.emit,
        )

    def set_entries(self, entries: list[dict], locale: str = "tr") -> None:
        self._entries = entries
        self._locale = locale
        self._server.ensure_running()
        self._server.set_html(build_map_html(entries, locale))
        self.load(QUrl(self._server.url_with_cache_bust()))

    def fly_to_book(self, book_id: int) -> None:
        self.page().runJavaScript(
            f"if (window.__kitapUx) {{ window.__kitapUx.markerT = Date.now(); }} "
            f"if (typeof window.flyToBook === 'function') {{ window.flyToBook({book_id}); }}"
        )
