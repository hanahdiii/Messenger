from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt
import shutil, os
from db import get_connection

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BH Messenger - Register")
        self.profile_pic_path = None
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("📝 ثبت‌نام در BH Messenger")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #ff80ab;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.input_username = QLineEdit()
        self.input_username.setPlaceholderText("نام کاربری")
        layout.addWidget(self.input_username)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("رمز عبور")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_password)

        self.input_confirm = QLineEdit()
        self.input_confirm.setPlaceholderText("تأیید رمز عبور")
        self.input_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input_confirm)

        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("شماره تلفن")
        layout.addWidget(self.input_phone)

        self.input_bio = QLineEdit()
        self.input_bio.setPlaceholderText("بیو (اختیاری)")
        layout.addWidget(self.input_bio)

        self.button_choose_pic = QPushButton("📷 انتخاب عکس پروفایل")
        self.button_choose_pic.clicked.connect(self.choose_profile_pic)
        layout.addWidget(self.button_choose_pic)

        self.button_submit = QPushButton("ثبت‌ نام")
        layout.addWidget(self.button_submit)
        self.button_submit.clicked.connect(self.register_user)

        self.setLayout(layout)

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
        


    def choose_profile_pic(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "انتخاب عکس", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            os.makedirs("profiles", exist_ok=True)
            filename = os.path.basename(file_path)
            dest_path = os.path.join("profiles", filename)
            shutil.copy(file_path, dest_path)
            self.profile_pic_path = dest_path
            self.button_choose_pic.setText("✅ عکس انتخاب شد")

    def register_user(self):
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()
        confirm = self.input_confirm.text().strip()
        phone = self.input_phone.text().strip()
        bio = self.input_bio.text().strip()
        profile_pic = self.profile_pic_path or ""  

        if not username or not password or not confirm:
            msg = QMessageBox()
            msg.setWindowTitle("خطا")
            msg.setText("لطفاً فیلدهای ضروری را پر کنید.")
            msg.setIcon(QMessageBox.Icon.Warning)
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
                }
            """)
            msg.exec()

            
            return

        if password != confirm:
            msg = QMessageBox()
            msg.setWindowTitle("خطا")
            msg.setText("رمزها با هم مطابقت ندارند.")
            msg.setIcon(QMessageBox.Icon.Warning)
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
                }
            """)
            msg.exec()

            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
                ALTER TABLE users ADD COLUMN bio TEXT
            """)
        except:
            pass  

        try:
            cur.execute("""
                UPDATE users SET bio = bio
            """) 
        except:
            pass

        try:
            cur.execute("""
                INSERT INTO users (username, password, phone, profile_pic, bio)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password, phone, profile_pic, bio))
            conn.commit()
            msg = QMessageBox()
            msg.setWindowTitle("خطا")
            msg.setText("موفقیت", "ثبت‌نام انجام شد!")
            msg.setIcon(QMessageBox.Icon.Warning)
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
                }
            """)
            msg.exec()
            self.close()
        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("خطا")
            msg.setText(f"خطا در ثبت‌نام:\n{e}")
            msg.setIcon(QMessageBox.Icon.Warning)
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
                }
            """)
            msg.exec()
        finally:
            conn.close()
