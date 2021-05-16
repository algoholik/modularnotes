from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QWidget, QVBoxLayout)
from services.monoa_service import monoa_service
from entities.snip import Snip
from entities.note import Note
from config import SETTINGS_FILE_PATH
from ui.monoa_note_container import MonoaNoteContainer
from ui.monoa_styles import CSS

class MonoaNoteViewer(QWidget):
    signal_note_updated = QtCore.pyqtSignal(Note)
    signal_snip_updated = QtCore.pyqtSignal(Snip)
    def __init__(self):
        super().__init__()
        self._setup_note_view()
        self.signal_note_updated.connect(self.update_note)

    def _setup_note_view(self) -> None:
        self.note_container = MonoaNoteContainer(
            # change this into the latest edited note after the sort-note-by-timestamp function is done
            monoa_service.get_note_by_id(monoa_service.get_latest_note_id())
        )
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.note_container)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

    def update_note(self, note: Note) -> None:
        print(note)
        self.note_container.update_note(note)
