from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QWidget, QVBoxLayout)
from entities.note import Note

class MonoaListItem(QWidget):
    '''
    Notes list item widget class
    '''
    signal_note_updated = QtCore.pyqtSignal(Note)
    signal_note_selected = QtCore.pyqtSignal(Note)
    def __init__(self, note: Note):
        super(MonoaListItem, self).__init__()

        self.note = note
        self.is_active = False

        self.setMaximumHeight(84)
        self.setContentsMargins(0,0,0,0)
        self.setAutoFillBackground(True)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: transparent;")

        self.note_title = QLabel("Untitled")
        self.note_content = QLabel("New note with no content")

        self.note_layout = QVBoxLayout()
        self.note_layout.addWidget(self.note_title)
        self.note_layout.addWidget(self.note_content)
        self.setLayout(self.note_layout)
        self.note_layout.setAlignment(Qt.AlignTop)

        self.note_title.setStyleSheet("font-size: 15px; font-weight: bold; margin: 0; padding: 0;")
        self.note_title.setMaximumWidth(320)
        self.note_content.setStyleSheet("font-size: 13px; font-weight: normal; margin: 0; padding: 0;")
        self.note_content.setWordWrap(True)
        self.note_content.setMaximumWidth(320)

        self.signal_note_updated.connect(self.update_note)

        # Update selected note list item.
        self.update_active_note_selection()

    def get_searchable_content(self) -> str:
        ''' Merge note id, name, content and datetime as one string to search from. '''
        note_snips_content = [snip.get_content() for snip in self.note.get_contents()]
        snips = " ".join(note_snips_content).replace("\n", " ").lower()
        searchable_content = f"{self.note.get_title().lower()} {snips}"
        return searchable_content

    def get_note_id(self) -> int:
        ''' Return note id. '''
        return self.note.get_id()

    def get_note_title(self) -> str:
        ''' Return note title. '''
        return self.note.get_title()

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
        note_title = self.note.get_title()
        note_contents = [snip.get_content() for snip in self.note.get_contents() if snip]
        note_snips_merged = " ".join(note_contents).replace("\n", " ").strip()[:80]
        if len(note_title) > 0:
            self.note_title.setText(f"{note_title}")
        else:
            self.note_title.setText("Untitled")
        if len(note_snips_merged) > 0:
            self.note_content.setText(f"{note_snips_merged}")
        else:
            self.note_content.setText("Empty note")

    def show(self) -> None:
        ''' Show note list item when matched in search. '''
        for element in [self, self.note_title, self.note_content]:
            element.setVisible(True)

    def hide(self) -> None:
        ''' Hide note list item when matched in search. '''
        for element in [self, self.note_title, self.note_content]:
            element.setVisible(False)

    def activate(self) -> None:
        ''' Set note item active in list. '''
        if self.is_active == False:
            self.is_active = True
        self.update_active_note_selection()

    def deactivate(self) -> None:
        ''' Set note item passive in list. '''
        self.is_active = False
        self.update_active_note_selection()

    def update_active_note_selection(self) -> None:
        ''' Active vs. passive note item styling. '''
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
