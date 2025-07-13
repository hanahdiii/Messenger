import sys
from PyQt6.QtWidgets import QApplication
from db import init_db
from ui_login import LoginWindow

if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
