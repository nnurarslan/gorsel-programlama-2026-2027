import sys
from PyQt5.QtWidgets import QApplication
from pages.login_page import LoginPage

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())
