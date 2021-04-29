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


class NoteListItem(QWidget):
    '''
    Notes list item widget class
    '''
    signal_note_selected = QtCore.pyqtSignal(Note)
    def __init__(self, note: Note):
        super(NoteListItem, self).__init__()

        self.note = note
        self.is_active = False

        self.setStyleSheet("color: #000000;")
        self.setMaximumHeight(84)
        self.setContentsMargins(0,0,0,0)
        self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: transparent;")

        self.note_name = QLabel("Untitled")
        self.note_content = QLabel("New note")

        self.note_layout = QVBoxLayout()
        self.note_layout.addWidget(self.note_name)
        self.note_layout.addWidget(self.note_content)
        self.setLayout(self.note_layout)
        self.note_layout.setAlignment(Qt.AlignTop)

        # Update selected note list item.
        self.update_active_note_selection()

        self.note_name.setStyleSheet("font-size: 15px; font-weight: bold; margin: 0; padding: 0;")
        self.note_name.setMaximumWidth(320)
        self.note_content.setStyleSheet("font-size: 13px; font-weight: normal; margin: 0; padding: 0;")
        self.note_content.setWordWrap(True)
        self.note_content.setMaximumWidth(320)

    def get_searchable_content(self) -> str:
        ''' Merge note id, name, content and datetime as one string to search from. '''
        all_note_content = [
            str(self.note.get_id()),
            self.note.get_name().replace("\n", "").strip(),
            self.note.get_content().replace("\n", "").strip()
        ]
        return " ".join(all_note_content).lower()

    def get_note_id(self) -> int:
        ''' Return note id. '''
        return self.note.get_id()

    def get_note_name(self) -> str:
        ''' Return note name. '''
        return self.note.get_name()

    def init_note(self, note: Note) -> None:
        ''' Initialize with given Note object and update note list item labels. '''
        self.note = note
        self._update_labels()

    def update_note(self, note: Note) -> None:
        ''' Update note object and update note list item labels. '''
        self.note = note
        self._update_labels()

    def _update_labels(self) -> None:
        ''' Update note list item labels. '''
        note_name_formatted = self.note.get_name().replace("\n", " ")[0:80]
        note_content_formatted = self.note.get_content().replace("\n", " ")[0:80]
        self.note_name.setText(f"{note_name_formatted}")
        self.note_content.setText(f"{note_content_formatted}")

    def show(self) -> None:
        ''' Show note list item when matched in search. '''
        for element in [self, self.note_name, self.note_content]:
            element.setVisible(True)

    def hide(self) -> None:
        ''' Hide note list item when matched in search. '''
        for element in [self, self.note_name, self.note_content]:
            element.setVisible(False)

    def activate(self) -> None:
        if self.is_active == False: 
            self.is_active = True
        self.update_active_note_selection()

    def deactivate(self) -> None:
        self.is_active = False
        self.update_active_note_selection()

    def update_active_note_selection(self) -> None:
        if self.is_active == True:
            self.setStyleSheet("color: #ffffff; background-color: #333333;")
        else:
            self.setStyleSheet("color: #333333; background-color: none;")

    def update_new_note_to_editor(self):
        ''' Update editor with selected note thru a PyQt signal. '''
        self.signal_note_selected.emit(self.note)

    def mousePressEvent(self, QMouseEvent) -> None:
        ''' On mouse click, update editor with selected note and make it active '''
        if QMouseEvent.button() == Qt.LeftButton:
            self.signal_note_selected.emit(self.note)
            self.activate()
        elif QMouseEvent.button() == Qt.RightButton:
            pass

    def keyReleaseEvent(self, QKeyEvent) -> None:
        ''' Keyboard shortcuts for note list area. '''
        if QKeyEvent:
            pass