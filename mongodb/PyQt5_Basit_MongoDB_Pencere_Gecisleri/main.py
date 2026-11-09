import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from pymongo.errors import PyMongoError
from database import check_connection, client
from pages.login_page import LoginPage

app = QApplication(sys.argv)
try:
    check_connection()
except PyMongoError as error:
    QMessageBox.critical(None, "Bağlantı Hatası", "MongoDB çalışıyor mu?\n" + str(error))
    sys.exit(1)

app.aboutToQuit.connect(client.close)
window = LoginPage()
window.show()
sys.exit(app.exec_())
