"""Minimal localhost HTTP server to serve generated Leaflet HTML to QWebEngineView.

Using http://127.0.0.1/... avoids several first-load races and size limits associated
with setHtml() on some Qt WebEngine builds.
"""

from __future__ import annotations

import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import ClassVar


class _MapRequestHandler(BaseHTTPRequestHandler):
    server_version = "KitapAtlasMap/1.0"

    def do_GET(self) -> None:
        if not self.path.startswith("/map"):
            self.send_error(404)
            return
        body = self.server.get_html_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store, must-revalidate")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args) -> None:
        return


class _ThreadingMapHTTPServer(ThreadingHTTPServer):
    def __init__(
        self,
        server_address: tuple[str, int],
        RequestHandlerClass: type[BaseHTTPRequestHandler],
        html_lock: threading.Lock,
        html_holder: list[bytes],
    ) -> None:
        self._html_lock = html_lock
        self._html_holder = html_holder
        super().__init__(server_address, RequestHandlerClass)

    def get_html_bytes(self) -> bytes:
        with self._html_lock:
            return self._html_holder[0]


class MapHttpServer:
    _singleton: ClassVar[MapHttpServer | None] = None
    _singleton_lock = threading.Lock()

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._holder: list[bytes] = [
            b"<!DOCTYPE html><html><head><meta charset='utf-8'/></head><body></body></html>"
        ]
        self._httpd: _ThreadingMapHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self._port: int = 0

    @classmethod
    def instance(cls) -> MapHttpServer:
        with cls._singleton_lock:
            if cls._singleton is None:
                cls._singleton = MapHttpServer()
            return cls._singleton

    def set_html(self, html: str) -> None:
        data = html.encode("utf-8")
        with self._lock:
            self._holder[0] = data

    def ensure_running(self) -> None:
        if self._httpd is not None:
            return
        server = _ThreadingMapHTTPServer(("127.0.0.1", 0), _MapRequestHandler, self._lock, self._holder)
        self._port = int(server.server_address[1])
        self._httpd = server
        self._thread = threading.Thread(target=server.serve_forever, daemon=True)
        self._thread.start()

    @property
    def map_url(self) -> str:
        if not self._port:
            raise RuntimeError("Map HTTP server not started")
        return f"http://127.0.0.1:{self._port}/map"

    def url_with_cache_bust(self) -> str:
        return f"{self.map_url}?t={time.time_ns()}"
