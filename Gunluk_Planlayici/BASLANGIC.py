"""Derste önce yalnızca arayüzü açmak için çalıştırın."""
import sys
from pathlib import Path
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
pencere = uic.loadUi(str(Path(__file__).with_name("planlayici.ui")))
pencere.show()
sys.exit(app.exec_())
