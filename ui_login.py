from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt

from db import get_connection
from ui_register import RegisterWindow
from ui_main import MainWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BH Messenger - Login")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🌸 BH Messenger 🌸")
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ff80ab;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("نام کاربری")
        layout.addWidget(self.input_username)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("رمز عبور")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("ورود")
        self.button_register = QPushButton("ثبت‌نام")
        layout.addWidget(self.button_login)
        layout.addWidget(self.button_register)

        self.setLayout(layout)

        self.button_login.clicked.connect(self.login)
        self.button_register.clicked.connect(self.open_register)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                font-family: "Segoe UI", "Vazirmatn", sans-serif;
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ff80ab;
                border-radius: 8px;
                color: white;
                background-color: #2a2a3b;
            }
            QPushButton {
                background-color: #ff80ab;
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f06292;
            }
        """)

    def login(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        if not username or not password:
            self.show_message("خطا", "لطفاً همه فیلدها را پر کنید.", QMessageBox.Icon.Warning)
            return

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            self.show_message("خوش آمدید", f"{username} عزیز خوش آمدی! 🎉", QMessageBox.Icon.Information)
            user_data = {"username": user[1], "phone": user[3]}
            self.main_window = MainWindow(current_user=user_data)
            self.main_window.show()
            self.close()
        else:
            self.show_message("خطا", "نام کاربری یا رمز اشتباه است.", QMessageBox.Icon.Critical)

    def open_register(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def show_message(self, title, text, icon=QMessageBox.Icon.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                color: white;
                font-family: "Vazirmatn", "Segoe UI";
                font-size: 14px;
            }
            QPushButton {
                background-color: #ffffff;
                color: white;
                border-radius: 6px;
                padding: 5px 10px;
            }
        """)
        msg.exec()
