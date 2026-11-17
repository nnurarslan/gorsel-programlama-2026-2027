from PyQt6.QtCore import QObject, QThread, pyqtSignal
import time


class RegisterViewModel(QObject):
    loading_changed = pyqtSignal(bool)
    error = pyqtSignal(str)
    register_success = pyqtSignal()

    def __init__(self, register_use_case):
        super().__init__()
        self.register_use_case = register_use_case
        self._thread = None
        self._worker = None

    def register(self, name: str, email: str, password: str):
        if self._thread is not None:
            return  # çift tıklamayı engelle

        print("[Register] start:", name, email)

        self.loading_changed.emit(True)

        self._thread = QThread()
        self._worker = RegisterWorker(
            self.register_use_case,
            name,
            email,
            password
        )

        self._worker.moveToThread(self._thread)

        # Worker lifecycle
        self._thread.started.connect(self._worker.run)

        self._worker.success.connect(self._on_success)
        self._worker.error.connect(self._on_error)

        # Cleanup
        self._worker.success.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup)

        self._thread.start()

    def _on_success(self):
        print("[Register] success")
        self.register_success.emit()

    def _on_error(self, message: str):
        print("[Register] error:", message)
        self.error.emit(message)

    def _cleanup(self):
        print("[Register] cleanup")
        self.loading_changed.emit(False)

        if self._worker:
            self._worker.deleteLater()
        if self._thread:
            self._thread.deleteLater()

        self._worker = None
        self._thread = None


class RegisterWorker(QObject):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, use_case, name, email, password):
        super().__init__()
        self.use_case = use_case
        self.name = name
        self.email = email
        self.password = password

    def run(self):
        try:
            # UX simülasyonu (opsiyonel)
            time.sleep(2)

            self.use_case.execute(
                self.name,
                self.email,
                self.password
            )

            self.success.emit()

        except Exception as e:
            self.error.emit(str(e))
