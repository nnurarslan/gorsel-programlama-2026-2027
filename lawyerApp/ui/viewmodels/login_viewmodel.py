from PyQt6.QtCore import QObject, QThread, pyqtSignal


class LoginViewModel(QObject):
    loading_changed = pyqtSignal(bool)
    error = pyqtSignal(str)
    login_success = pyqtSignal()

    def __init__(self, login_use_case):
        super().__init__()
        self.login_use_case = login_use_case
        self._thread = None
        self._worker = None

    def login(self, email, password, remember):
        if self._thread is not None:
            return  # Çift tıklamayı engelle

        print(email, password, remember)

        self.loading_changed.emit(True)

        self._thread = QThread()
        self._worker = LoginWorker(
            self.login_use_case,
            email,
            password,
            remember
        )

        self._worker.moveToThread(self._thread)

        # SIGNALS
        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(self._on_success)
        self._worker.error.connect(self._on_error)

        # CLEANUP
        self._worker.success.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup)

        self._thread.start()

    def _on_success(self):
        self.login_success.emit()

    def _on_error(self, message):
        self.error.emit(message)

    def _cleanup(self):
        self.loading_changed.emit(False)
        self._worker.deleteLater()
        self._thread.deleteLater()
        self._worker = None
        self._thread = None



import time
from PyQt6.QtCore import QObject, pyqtSignal


class LoginWorker(QObject):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, use_case, email, password, remember):
        super().__init__()
        self.use_case = use_case
        self.email = email
        self.password = password
        self.remember = remember

    def run(self):
        try:
            print("Login başladı, 3 sn bekleniyor...")
            time.sleep(3)  # ⏳ 3 saniye beklet

            self.use_case.execute(
                self.email,
                self.password,
                self.remember
            )

            print("Login başarılı")
            self.success.emit()

        except Exception as e:
            self.error.emit(str(e))
