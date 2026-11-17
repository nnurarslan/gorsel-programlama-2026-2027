from PyQt6.QtCore import QObject, QThread, pyqtSignal


class LawCategoriesViewModel(QObject):
    loading_changed = pyqtSignal(bool)
    error = pyqtSignal(str)
    data_loaded = pyqtSignal(list)  # list[LawCategoryDTO]

    def __init__(self, use_case):
        super().__init__()
        self.use_case = use_case

        self._thread = None
        self._worker = None

    def load(self):
        # Çift tıklamayı engelle
        if self._thread is not None:
            return

        self.loading_changed.emit(True)

        self._thread = QThread()
        self._worker = LawCategoriesWorker(self.use_case)

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

    def _on_success(self, categories):
        self.data_loaded.emit(categories)

    def _on_error(self, message):
        self.error.emit(message)

    def _cleanup(self):
        self.loading_changed.emit(False)

        self._worker.deleteLater()
        self._thread.deleteLater()

        self._worker = None
        self._thread = None



class LawCategoriesWorker(QObject):
    success = pyqtSignal(list)  # list[LawCategoryDTO]
    error = pyqtSignal(str)

    def __init__(self, use_case):
        super().__init__()
        self.use_case = use_case

    def run(self):
        try:
            categories = self.use_case.execute()
            self.success.emit(categories)

        except Exception as e:
            self.error.emit(str(e))
