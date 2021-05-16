from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout, QLineEdit, QWidget, QPushButton, QVBoxLayout, QScrollArea
)
from services.monoa_service import monoa_service
from entities.note import Note
from ui.monoa_list_item import MonoaListItem

class MonoaBrowser(QWidget):
    '''
    Monoa Note browser class
    '''
    signal_note_selected = QtCore.pyqtSignal(Note)
    signal_note_updated = QtCore.pyqtSignal(Note)
    def __init__(self):
        super().__init__()
        self.setMaximumWidth(360)
        self.notes = QWidget()
        self.notes_layout = QVBoxLayout()
        self.notes_layout.setDirection(QVBoxLayout.TopToBottom)
        self.notes_layout.addStretch()

        self.notes_list_items = []
        self.notes_dict = {}

        for note in monoa_service.get_notes():
            item = MonoaListItem(self)
            item.init_note(note)
            item.signal_note_selected.connect(self._signal_handler_note_selected)
            self.notes_layout.insertWidget(0, item)
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

        # Search field and New button
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Search notes...")
        self.input_search.textChanged.connect(self._update_search_results)
        self.input_search.setClearButtonEnabled(True)
        self.btn_new_note = QPushButton()
        self.btn_new_note.setText("Create Note")
        self.btn_new_note.clicked.connect(self._new_note)
        self.toolbar_hbox = QHBoxLayout()
        self.toolbar_hbox.addWidget(self.input_search)
        self.toolbar_hbox.addWidget(self.btn_new_note)
        self.toolbar = QWidget()
        self.toolbar.setLayout(self.toolbar_hbox)
        self.toolbar_hbox.setContentsMargins(0,0,0,0)
        self.toolbar_hbox.setSpacing(15)

        container_layout = QVBoxLayout()
        container_layout.addWidget(self.toolbar)
        container_layout.addWidget(self.scroll)
        self.setLayout(container_layout)

        # Activate last modified note item in list
        self._activate_latest_on_load()

    def _update_search_results(self, text) -> None:
        for note in self.notes_list_items:
            if text.lower() in note.get_searchable_content():
                note.show()
            else:
                note.hide()

    def _new_note(self) -> None:
        new_note = monoa_service.create_note("")
        item = MonoaListItem(self)
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

    def _activate_latest_on_load(self) -> None:
        for item in self.notes_list_items:
            if item.get_note_id() == monoa_service.get_latest_note_id():
                item.activate()

    def _signal_handler_note_selected(self, note: Note) -> None:
        self.signal_note_selected.emit(note)
        for item in self.notes_list_items:
            if item.get_note_id() != note.get_id():
                item.deactivate()

    def update_active_note(self, note_updated: Note) -> None:
        for item in self.notes_list_items:
            if item.get_note_id() == note_updated.get_id():
                item.update_note(note_updated)
