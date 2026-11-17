from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import QPropertyAnimation, QRect


class SpinnerWidget(QLabel):
    def __init__(self, size=28, parent=None):
        super().__init__(parent)

        self.setFixedSize(size, size)
        self.setStyleSheet(f"""
            QLabel {{
                border: 3px solid #1e293b;
                border-top: 3px solid #2563eb;
                border-radius: {size // 2}px;
                background: transparent;
            }}
        """)

        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(900)
        self._anim.setLoopCount(-1)

        self.hide()

    def start(self):
        self.show()
        rect = self.geometry()
        self._anim.setStartValue(rect)
        self._anim.setEndValue(rect)
        self._anim.start()

    def stop(self):
        self._anim.stop()
        self.hide()
