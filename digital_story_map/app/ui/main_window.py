from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QStatusBar,
    QWidget,
)

from app.i18n import t
from app.services.data_service import DataService
from app.ui.about_dialog import AboutDialog
from app.ui.admin_dialog import AdminLoginDialog
from app.ui.book_list_dialog import BookListDialog
from app.ui.map_container import MapWithSearchOverlay
from app.ui.sidebar import SidebarWidget
from app.ui.statistics_dialog import StatisticsDialog


class MainWindow(QMainWindow):
    """Emitted once after the first successful or failed dataset load (startup gate for splash)."""

    startup_ready = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.resize(1300, 820)

        self.entries: list[dict] = []
        self._locale: str = "tr"
        self.setWindowTitle(t(self._locale, "app_title"))
        self._stats_dialog: StatisticsDialog | None = None
        self._startup_notified = False

        self.sidebar = SidebarWidget()
        self.map_stack = MapWithSearchOverlay()

        self.sidebar.book_catalog_requested.connect(self._open_book_list)
        self.sidebar.about_requested.connect(self._open_about)
        self.sidebar.stats_requested.connect(self._open_stats)
        self.sidebar.locale_changed.connect(self._on_locale_changed)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.map_stack)
        splitter.setSizes([300, 1000])

        central = QWidget()
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)
        self.setCentralWidget(central)

        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status.showMessage(t(self._locale, "status_loading"))

        self.data_service = DataService()
        self.data_service.loaded.connect(self._on_data_loaded)
        self.data_service.failed.connect(self._on_data_failed)

        self.map_stack.set_entries([], self._locale)
        QTimer.singleShot(0, self.data_service.load_async)
        QShortcut(QKeySequence("Ctrl+Shift+A"), self, activated=self._open_admin_login)

    def _on_data_loaded(self, entries: list[dict], from_cache: bool, message: str) -> None:
        self.entries = entries
        self.map_stack.set_entries(entries, self._locale)
        mode = "CACHE" if from_cache else "LIVE"
        self.status.showMessage(f"{message} [{mode}]")
        self._emit_startup_ready()

    def _on_data_failed(self, message: str) -> None:
        self.status.showMessage(message)
        QMessageBox.warning(self, t(self._locale, "msg_data_error"), message)
        self._emit_startup_ready()

    def _emit_startup_ready(self) -> None:
        if self._startup_notified:
            return
        self._startup_notified = True
        self.startup_ready.emit()

    def _on_locale_changed(self, locale: str) -> None:
        self._locale = locale if locale in ("tr", "en") else "tr"
        self.setWindowTitle(t(self._locale, "app_title"))
        self.map_stack.apply_language(self._locale)
        if self.entries:
            self.map_stack.set_entries(self.entries, self._locale)

    def _open_book_list(self) -> None:
        dlg = BookListDialog(self.entries, self, self._locale)
        dlg.book_selected.connect(self.map_stack.map_view.fly_to_book)
        dlg.exec()

    def _open_about(self) -> None:
        AboutDialog(self, self._locale).exec()

    def _open_stats(self) -> None:
        self._stats_dialog = StatisticsDialog(self.entries, self, self._locale)
        self._stats_dialog.exec()

    def _open_admin_login(self) -> None:
        dialog = AdminLoginDialog(self)
        if dialog.exec() and dialog.authenticated:
            QMessageBox.information(
                self,
                "Admin Vault",
                "Admin authentication successful.\nAdmin management tools will be enabled in next step.",
            )
