from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QListWidget, QListWidgetItem, QMessageBox, QHBoxLayout
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
import os
from db import get_connection
from ui_chat import ChatWindow
from my_profile_dialog import MyProfileDialog

class MainWindow(QWidget):
    def __init__(self, current_user):
        super().__init__()
        self.setWindowTitle("BH Messenger - Home")
        self.current_user = current_user
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🌸 BH Messenger 🌸")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ff80ab;")
        layout.addWidget(title)

        user_info = QLabel(f"ورود با کاربر: <b>{self.current_user['username']}</b>")
        user_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        user_info.setStyleSheet("color: white;")
        layout.addWidget(user_info)

        self.users_list = QListWidget()
        self.users_list.setIconSize(QSize(36, 36))
        self.users_list.setStyleSheet("""
            QListWidget {
                background-color: #2a2a3b;
                color: white;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        
        layout.addWidget(self.users_list)

        self.button_chat = QPushButton("💬 شروع چت")
        layout.addWidget(self.button_chat)
        self.button_chat.clicked.connect(self.open_chat)

        self.button_profile = QPushButton("👤 پروفایل من")
        layout.addWidget(self.button_profile)
        self.button_profile.clicked.connect(self.open_profile)

        self.setLayout(layout)
        self.load_users()

        self.setStyleSheet("""
            QWidget {
                background-color:rgb(48, 46, 46);
                font-family: "Segoe UI", "Vazirmatn", sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color:rgb(228, 109, 155);
                color: white;
                padding: 8px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color:rgb(204, 86, 141);
            }
        """)
    def load_users(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT username, profile_pic FROM users WHERE username != ?", (self.current_user['username'],))
        users = cur.fetchall()
        conn.close()

        self.users_list.clear()

        for username, pic_path in users:
            item = QListWidgetItem(username)

            if pic_path and os.path.exists(pic_path):
                icon = QIcon(QPixmap(pic_path).scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio))
                item.setIcon(icon)
            else:
                default_icon = QIcon(QPixmap("default_avatar.png").scaled(36, 36, Qt.AspectRatioMode.KeepAspectRatio))
                item.setIcon(default_icon)

            self.users_list.addItem(item)

    def open_chat(self):
        selected = self.users_list.currentItem()
        if not selected:
            msg = QMessageBox()
            msg.setWindowTitle("خطا")
            msg.setText("لطفاً یک کاربر را برای چت انتخاب کنید.")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStyleSheet("""
                                QMessageBox {
                                    background-color: #1e1e2f;
                                    color: white;
                                    font-family: Segoe UI;
                                    font-size: 14px;
                                }
                                QPushButton {
                                    background-color: #ff80ab;
                                    color: white;
                                    border-radius: 6px;
                                }
                            """)
            msg.exec()
            return

        receiver_username = selected.text()
        self.chat_window = ChatWindow(sender=self.current_user['username'], receiver=receiver_username)
        self.chat_window.show()

    def open_profile(self):
        dlg = MyProfileDialog(self.current_user['username'])
        dlg.exec()
        self.load_users()
