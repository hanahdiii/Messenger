from PyQt6.QtWidgets import (
    QDialog, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtCore import Qt
import os, shutil
from db import get_connection

class MyProfileDialog(QDialog):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle("پروفایل من")
        self.username = username
        self.profile_pic_path = ""
        self.init_ui()
        self.load_user_info()

    def init_ui(self):
        self.setMinimumSize(400, 400)
        layout = QVBoxLayout()

        self.pic_label = QLabel()
        self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pic_label.setFixedSize(180, 180)
        self.pic_label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(self.pic_label)

        self.button_change = QPushButton("📷 تغییر عکس")
        self.button_delete = QPushButton("🗑 حذف عکس")
        self.button_save = QPushButton("💾 ذخیره تغییرات")

        self.input_bio = QLineEdit()
        self.input_bio.setPlaceholderText("بیو جدید خود را وارد کنید...")

        btn_row = QHBoxLayout()
        btn_row.addWidget(self.button_change)
        btn_row.addWidget(self.button_delete)

        layout.addWidget(self.input_bio)
        layout.addLayout(btn_row)
        layout.addWidget(self.button_save)

        self.setLayout(layout)

        self.button_change.clicked.connect(self.change_pic)
        self.button_delete.clicked.connect(self.delete_pic)
        self.button_save.clicked.connect(self.save_profile)

        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
                color: white;
                font-family: "Vazirmatn", "Shabnam", "Segoe UI";
            }
            QLineEdit {
                padding: 10px;
                background-color: #2a2a3b;
                color: white;
                border: 1px solid #ff80ab;
                border-radius: 8px;
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

    def load_user_info(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT profile_pic, bio FROM users WHERE username = ?", (self.username,))
        result = cur.fetchone()
        conn.close()

        self.profile_pic_path = result[0] if result and result[0] else ""
        bio = result[1] if result else ""

        self.input_bio.setText(bio)
        self.show_pic()

    def show_pic(self):
        if self.profile_pic_path and os.path.exists(self.profile_pic_path):
            pixmap = QPixmap(self.profile_pic_path).scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio)
        else:
            pixmap = QPixmap("default_avatar.png").scaled(160, 160, Qt.AspectRatioMode.KeepAspectRatio)

        self.pic_label.setPixmap(pixmap)

    def change_pic(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "انتخاب عکس جدید", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            os.makedirs("profiles", exist_ok=True)
            filename = f"{self.username}_{os.path.basename(file_path)}"
            dest_path = os.path.join("profiles", filename)
            shutil.copy(file_path, dest_path)
            self.profile_pic_path = dest_path
            self.show_pic()

    def delete_pic(self):
        self.profile_pic_path = ""
        self.show_pic()

    def save_profile(self):
        bio = self.input_bio.text().strip()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE users SET profile_pic = ?, bio = ? WHERE username = ?
        """, (self.profile_pic_path, bio, self.username))
        conn.commit()
        conn.close()
        QMessageBox.information(self, "ذخیره شد", "تغییرات پروفایل با موفقیت ذخیره شد!")
        self.close()
