from hashlib import sha256

from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class AdminLoginDialog(QDialog):
    """
    Placeholder login dialog for future Admin Vault implementation.
    Default password for demonstration is: admin123
    """

    PASSWORD_HASH = sha256("admin123".encode("utf-8")).hexdigest()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Admin Vault")
        self.resize(320, 160)
        self._authenticated = False

        self.info = QLabel("Enter admin password")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.status_label = QLabel("")

        self.login_button = QPushButton("Unlock")
        self.cancel_button = QPushButton("Cancel")
        self.login_button.clicked.connect(self._check_password)
        self.cancel_button.clicked.connect(self.reject)

        form = QFormLayout()
        form.addRow("Password:", self.password_input)

        row = QHBoxLayout()
        row.addWidget(self.cancel_button)
        row.addWidget(self.login_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.info)
        layout.addLayout(form)
        layout.addWidget(self.status_label)
        layout.addLayout(row)

    @property
    def authenticated(self) -> bool:
        return self._authenticated

    def _check_password(self) -> None:
        candidate = self.password_input.text().encode("utf-8")
        if sha256(candidate).hexdigest() == self.PASSWORD_HASH:
            self._authenticated = True
            self.accept()
            return
        self.status_label.setText("Invalid password.")
