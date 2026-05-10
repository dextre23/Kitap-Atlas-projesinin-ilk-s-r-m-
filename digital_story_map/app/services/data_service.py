import json
from pathlib import Path
from typing import Any

import requests
from PySide6.QtCore import QObject, QRunnable, QThreadPool, Signal

from app.config import CACHE_FILE, DATA_URL
from app.models import BookEntry


class DataSignals(QObject):
    loaded = Signal(list, bool, str)
    failed = Signal(str)


class DataFetchWorker(QRunnable):
    def __init__(self, url: str, cache_file: Path) -> None:
        super().__init__()
        self.url = url
        self.cache_file = cache_file
        self.signals = DataSignals()

    def run(self) -> None:
        payload: list[dict[str, Any]] | None = None
        from_cache = False
        message = ""

        try:
            response = requests.get(self.url, timeout=7)
            response.raise_for_status()
            payload = response.json()
            self._write_cache(payload)
            message = "Remote data loaded successfully."
        except requests.RequestException:
            payload = self._read_cache()
            from_cache = True
            message = "Offline mode: cached data loaded."
        except (ValueError, TypeError):
            payload = self._read_cache()
            from_cache = True
            message = "Remote payload invalid, fallback to cache."

        if payload is None:
            self.signals.failed.emit("No remote or cached data available.")
            return

        entries = [BookEntry.from_dict(item).to_dict() for item in payload]
        self.signals.loaded.emit(entries, from_cache, message)

    def _write_cache(self, payload: list[dict[str, Any]]) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache_file.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _read_cache(self) -> list[dict[str, Any]] | None:
        if not self.cache_file.exists():
            return None
        try:
            return json.loads(self.cache_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None


class DataService(QObject):
    loaded = Signal(list, bool, str)
    failed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._pool = QThreadPool.globalInstance()

    def load_async(self, url: str = DATA_URL, cache_file: Path = CACHE_FILE) -> None:
        worker = DataFetchWorker(url=url, cache_file=cache_file)
        worker.signals.loaded.connect(self.loaded.emit)
        worker.signals.failed.connect(self.failed.emit)
        self._pool.start(worker)
