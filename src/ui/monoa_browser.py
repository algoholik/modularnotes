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

from ui.note_list_item import NoteListItem

class MonoaBrowser(QWidget):
    '''
    Monoa Layout class
    '''
    signal_note_selected = QtCore.pyqtSignal(Note)
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(360)
        self.notes = QWidget()
        self.notes_layout = QVBoxLayout()

        self.notes_list_items = []
        self.notes_dict = {}

        for note in monoa_service.get_notes():
            item = NoteListItem(self)
            item.init_note(note)
            item.signal_note_selected.connect(self._signal_handler_note_selected)
            self.notes_layout.addWidget(item)
            self.notes_list_items.append(item)

        self.notes.setLayout(self.notes_layout)
        self.notes_layout.setContentsMargins(0,0,0,0)
        self.notes_layout.setSpacing(0)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.notes)

        # Tool bar
        self.notes_toolbar = QPushButton()
        self.notes_toolbar.setText("New note")
        self.notes_toolbar.clicked.connect(self._new_note)

        # Search bar
        self.notes_searchbar = QLineEdit()
        self.notes_searchbar.setPlaceholderText("Search notes...") 
        self.notes_searchbar.textChanged.connect(self._update_search_results)

        container_layout = QVBoxLayout()
        container_layout.addWidget(self.notes_toolbar)
        container_layout.addWidget(self.notes_searchbar)
        container_layout.addWidget(self.scroll)
        self.setLayout(container_layout)

    def _update_search_results(self, text) -> None:
        for note in self.notes_list_items:
            if text.lower() in note.get_searchable_content():
                note.show()
            else:
                note.hide()

    def _new_note(self) -> None:
        new_note = monoa_service.create_note("Untitled", "New note", datetime.now())
        item = NoteListItem(self)
        item.init_note(new_note)
        item.signal_note_selected.connect(self._signal_handler_note_selected)
        self.notes_layout.insertWidget(0, item)
        self.notes_list_items.append(item)
        for item in self.notes_list_items:
            if item.get_note_id() == new_note.get_id():
                item.activate()
                item.update_new_note_to_editor()
            else:
                item.deactivate()

    def _signal_handler_note_selected(self, note: Note) -> None:
        self.signal_note_selected.emit(note)
        for item in self.notes_list_items:
            if item.get_note_id() != note.get_id():
                item.deactivate()

    def update_active_note(self, note_updated: Note) -> None:
        for note in self.notes_list_items:
            if note.get_note_id() == note_updated.get_id():
                note.update_note(note_updated)