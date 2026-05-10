import sys
import time
from pathlib import Path

from PySide6.QtCore import QAbstractAnimation, QEasingCurve, QCoreApplication, QPropertyAnimation, QTimer, Qt
from PySide6.QtWidgets import QApplication

from app.config import APP_NAME
from app.ui.animated_splash import AnimatedSplashScreen
from app.ui.main_window import MainWindow


def load_stylesheet() -> str:
    qss_path = Path(__file__).parent / "app" / "resources" / "dark_theme.qss"
    if not qss_path.exists():
        return ""
    return qss_path.read_text(encoding="utf-8")


def _fade_in_window(window: MainWindow, duration_ms: int = 650) -> None:
    window.setWindowOpacity(0.0)
    anim = QPropertyAnimation(window, b"windowOpacity", window)
    anim.setDuration(duration_ms)
    anim.setStartValue(0.0)
    anim.setEndValue(1.0)
    anim.setEasingCurve(QEasingCurve.Type.OutCubic)
    anim.start(QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)


def main() -> int:
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts, True)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(load_stylesheet())

    splash = AnimatedSplashScreen()
    splash.show()
    app.processEvents()
    splash_start = time.monotonic()

    window = MainWindow()
    window.hide()

    min_splash_s = 1.35

    def reveal() -> None:
        elapsed = time.monotonic() - splash_start
        remaining_ms = max(0, int((min_splash_s - elapsed) * 1000))

        def finish_splash_and_show() -> None:
            splash.close()
            window.show()
            app.processEvents()
            _fade_in_window(window)

        QTimer.singleShot(remaining_ms, finish_splash_and_show)

    window.startup_ready.connect(reveal)

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
