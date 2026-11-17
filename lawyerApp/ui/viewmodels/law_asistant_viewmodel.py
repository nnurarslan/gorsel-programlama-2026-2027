from PyQt6.QtCore import QObject, QThread, pyqtSignal
from application.dto.law_asistant_dto import LawAssistantResponseDTO
from application.use_cases.law_asistant_use_case import LawAssistantUseCase
from core.session.session_manager import SessionManager
import json


class LawAssistantViewModel(QObject):
    loading_changed = pyqtSignal(bool)
    response_loaded = pyqtSignal(LawAssistantResponseDTO)
    error = pyqtSignal(str)

    def __init__(self, use_case: LawAssistantUseCase):
        super().__init__()
        self.use_case = use_case
        self._thread = None
        self._worker = None

    def ask_question(self, question: str, law_category_id: int):
        if self._thread is not None:
            return

        self.loading_changed.emit(True)

        self._thread = QThread()
        self._worker = LawAssistantWorker(self.use_case, question, law_category_id)
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.success.connect(self._on_success)
        self._worker.error.connect(self._on_error)
        self._worker.success.connect(self._thread.quit)
        self._worker.error.connect(self._thread.quit)
        self._thread.finished.connect(self._cleanup)

        self._thread.start()

    def _on_success(self, data: LawAssistantResponseDTO):
        self.response_loaded.emit(data)

    def _on_error(self, message: str):
        self.error.emit(message)

    def _cleanup(self):
        self.loading_changed.emit(False)
        if self._worker:
            self._worker.deleteLater()
        if self._thread:
            self._thread.deleteLater()
        self._worker = None
        self._thread = None


class LawAssistantWorker(QObject):
    success = pyqtSignal(LawAssistantResponseDTO)
    error = pyqtSignal(str)

    def __init__(self, use_case: LawAssistantUseCase, question: str, law_category_id: int):
        super().__init__()
        self.use_case = use_case
        self.question = question
        self.law_category_id = law_category_id

        # Token artık doğrudan SessionManager'dan alınıyor
        user_raw = SessionManager.user()
        if isinstance(user_raw, str):
            try:
                user = json.loads(user_raw)
            except json.JSONDecodeError:
                user = {}
        else:
            user = user_raw
        self.token = user.get("accessToken", "")

    def run(self):
        try:
            result = self.use_case.execute(self.question, self.law_category_id, self.token)
            self.success.emit(result)
        except Exception as e:
            self.error.emit(str(e))
