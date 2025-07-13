from PyQt6.QtWidgets import (
    QWidget, QLabel, QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import os
from db import get_connection
from client_socket import ChatClient

class ChatWindow(QWidget):
    def __init__(self, sender, receiver):
        super().__init__()
        self.setWindowTitle("BH Messenger 💖")
        self.sender = sender
        self.receiver = receiver
        self.chat_client = ChatClient(self.sender, self.receive_message)

        self.setup_ui()
        self.load_messages()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.label_title = QLabel("🌸 BH Messenger 🌸")
        self.label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_title.setStyleSheet("font-size: 22px; font-weight: bold; color: #ff80ab;")
        layout.addWidget(self.label_title)

        self.label_user = QLabel(f"چت با: <b>{self.receiver}</b>")
        self.label_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_user.setStyleSheet("color: white;")
        layout.addWidget(self.label_user)

        self.chat_history = QTextBrowser()
        self.chat_history.setOpenExternalLinks(True)
        self.chat_history.setStyleSheet("background-color: #1e1e2f; color: white; border-radius: 10px; padding: 10px;")
        layout.addWidget(self.chat_history)

        input_layout = QHBoxLayout()
        self.input_message = QLineEdit()
        self.input_message.setPlaceholderText("💬 پیام خود را بنویسید...")
        self.button_send = QPushButton("💖 ارسال")

        input_layout.addWidget(self.input_message)
        input_layout.addWidget(self.button_send)
        layout.addLayout(input_layout)

        self.setLayout(layout)
        self.button_send.clicked.connect(self.send_message)

        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                font-family: "Vazirmatn", "Shabnam", "Segoe UI", sans-serif;
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
                padding: 8px 14px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f06292;
            }
        """)

    def get_profile_pic_path(self, username):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT profile_pic FROM users WHERE username = ?", (username,))
        result = cur.fetchone()
        conn.close()
        return result[0] if result and result[0] and os.path.exists(result[0]) else "default_avatar.png"

    def append_message(self, sender, content, timestamp=None):
        pic_path = self.get_profile_pic_path(sender)
        img_html = f'<img src="{pic_path}" width="24" height="24" style="border-radius:12px; vertical-align: middle;">'

        if sender == self.sender:
            msg_html = f"""
            <div style="text-align: right; margin: 10px;">
                <div style="display: inline-flex; align-items: center; gap: 6px;">
                    <div style="background-color: #ff99cc; padding: 10px; border-radius: 10px; color: white; max-width: 70%;">
                        {content}
                    </div>
                    {img_html}
                </div><br>
                <small style="color: #e0e0e0;">{timestamp or ""}</small>
            </div>
            """
        else:
            msg_html = f"""
            <div style="text-align: left; margin: 10px;">
                <div style="display: inline-flex; align-items: center; gap: 6px;">
                    {img_html}
                    <div style="background-color: #607d8b; padding: 10px; border-radius: 10px; color: white; max-width: 70%;">
                        <b>{sender}</b>: {content}
                    </div>
                </div><br>
                <small style="color: #cfcfcf;">{timestamp or ""}</small>
            </div>
            """
        self.chat_history.append(msg_html)

    def load_messages(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            SELECT sender, content, timestamp FROM messages
            WHERE (sender = ? AND receiver = ?)
               OR (sender = ? AND receiver = ?)
            ORDER BY timestamp ASC
        ''', (self.sender, self.receiver, self.receiver, self.sender))
        messages = cur.fetchall()
        conn.close()

        self.chat_history.clear()
        for sender, content, timestamp in messages:
            self.append_message(sender, content, timestamp)

    def receive_message(self, full_data):
        try:
            sender, content = full_data.split(":", 1)
            self.append_message(sender, content)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
                (sender, self.sender, content)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[ERROR] دریافت پیام شکست خورد: {e}")

    def send_message(self):
        content = self.input_message.text().strip()
        if not content:
            return

        self.chat_client.send(self.receiver, content)

        self.append_message(self.sender, content)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (sender, receiver, content) VALUES (?, ?, ?)",
            (self.sender, self.receiver, content)
        )
        conn.commit()
        conn.close()

        self.input_message.clear()

    def closeEvent(self, event):
        self.chat_client.close()
        event.accept()
