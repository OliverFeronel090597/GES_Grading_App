from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

class PasswordLoginWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_x = parent

        self.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                padding-right: 32px;
                border: 1px solid #c8c8c8;
                border-radius: 6px;
                background: #ffffff;
                color: #222;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #2994ff;
            }

            QPushButton#loginBtn {
                background: #2994ff;
                color: white;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton#loginBtn:hover {
                background: #1f7ed4;
            }
            QPushButton#loginBtn:pressed {
                background: #1664aa;
            }
        """)

        # Username
        self.username = QLineEdit()
        self.username.setPlaceholderText("Username")

        # Password
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)

        # Show/Hide eye button
        self.show_icon = QIcon("img/Show.png")
        self.hide_icon = QIcon("img/Hide.png")

        self.toggle_btn = QPushButton(self.password)
        self.toggle_btn.setIcon(self.show_icon)
        self.toggle_btn.setFlat(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.setFixedSize(24, 24)
        self.toggle_btn.setStyleSheet("border: none; background: transparent;")

        self.password.resizeEvent = self._resize_button
        self.toggle_btn.clicked.connect(self.toggle_password)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("loginBtn")
        self.login_btn.clicked.connect(self.print_credentials)

        # ENTER triggers login
        self.username.returnPressed.connect(self.print_credentials)
        self.password.returnPressed.connect(self.print_credentials)
        self.login_btn.setDefault(True)  # ENTER on button

        # Layout
        main = QVBoxLayout(self)
        main.setSpacing(12)
        main.addWidget(self.username)
        main.addWidget(self.password)
        main.addWidget(self.login_btn)

    def _resize_button(self, event):
        self.toggle_btn.move(self.password.width() - 28, (self.password.height() - 24) // 2)

    def toggle_password(self):
        if self.password.echoMode() == QLineEdit.EchoMode.Password:
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setIcon(self.hide_icon)
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setIcon(self.show_icon)

    def print_credentials(self):
        print("Username:", self.username.text())
        print("Password:", self.password.text())
        self.parent_x.show()


# Run
if __name__ == "__main__":
    app = QApplication([])

    win = QWidget()
    layout = QVBoxLayout(win)
    form = PasswordLoginWidget()

    layout.addWidget(form)
    win.setWindowTitle("Login Example")
    win.resize(300, 180)
    win.show()

    app.exec()
