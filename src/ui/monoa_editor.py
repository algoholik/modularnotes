from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import (
    QMainWindow,    QLabel,             QListWidget,
    QStatusBar,     QLineEdit,          QMenu,
    QAction,        QTabWidget,         QDockWidget,
    QFormLayout,    QWidget,            QHBoxLayout,
    QTextEdit,      QToolBar,           QPushButton,
    QVBoxLayout,    QSpacerItem,        QSizePolicy,
    QScrollArea,    QCompleter,         QButtonGroup
    )
from services.monoa_service import monoa_service
from entities.snip import Snip
from entities.note import Note
from config import SETTINGS_FILE_PATH
import utils

class MonoaEditor(QVBoxLayout):
    '''
    Monoa note editor UI class
    '''
    signal_note_updated = QtCore.pyqtSignal(Note)
    def __init__(self, note: Note) -> None:
        super().__init__()
        self.note = note
        self.note_id = QLabel(f"#{str(self.note.get_id())}")
        self.note_name = QLineEdit()
        self.note_content = QTextEdit()
        self.note_content.setAcceptRichText(False)
        self.addWidget(self.note_id)
        self.addWidget(self.note_name)
        self.addWidget(self.note_content)

        self.note_name.setStyleSheet("font-size: 20px; font-weight: bold; border: 0px; background: transparent;")

        self.note_name.setPlaceholderText("Untitled")
        self.note_content.setPlaceholderText("New note")

        self._update_editor()

        self.note_name.textChanged.connect(self._save_name)
        self.note_content.textChanged.connect(self._save_content)

    def update_note(self, note: Note) -> None:
        ''' Loads MonoaEditor with a new Note object. '''
        self.note = note
        self._update_editor()

    def _update_editor(self) -> None:
        self.note_id.setText(f"{str(self.note.get_id())}")
        self.note_name.setText(self.note.get_name())
        self.note_content.setPlainText(self.note.get_content())

    def _save_name(self) -> None:
        self.note.set_name(self.note_name.text())
        self._update_browser_note()

    def _save_content(self) -> None:
        self.note.set_content(self.note_content.toPlainText())
        self._update_browser_note()

    def _update_browser_note(self) -> None:
        self.signal_note_updated.emit(self.note)
        monoa_service.update_note(self.note)