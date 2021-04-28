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

# Globals
MONOA_WINDOW_TITLE = "MoNoA"
MONOA_RELEASE = "MoNoA Modular Notes App (Version 0.3.0 early bird alpha)"


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


class MonoaUI(QWidget):
    '''
    Monoa Layout class
    '''
    signal_note_selected = QtCore.pyqtSignal(Note)
    def __init__(self):
        super().__init__()

        self.monoa_layout = QHBoxLayout()
        self.setLayout(self.monoa_layout)

        self.monoa_browser = MonoaBrowser()
        self.monoa_editor = MonoaEditor(monoa_service.get_notes()[0])
        self.monoa_layout.addWidget(self.monoa_browser)
        self.monoa_layout.addLayout(self.monoa_editor)

        # PyQt Signals that update note under editing
        self.monoa_browser.signal_note_selected.connect(self._signal_handler_note_selected)
        self.monoa_editor.signal_note_updated.connect(self._signal_handler_note_updated)

    def _signal_handler_note_selected(self, note):
        self.monoa_editor.update_note(note)

    def _signal_handler_note_updated(self, note):
        self.monoa_browser.update_active_note(note)
        self.parent().update_window(note)


class MonoaMainWindow(QMainWindow):
    '''
    MonoaMainWindow class
    '''
    def __init__(self, parent=None, **params):
        super().__init__(parent)
        # Set main window title and size
        self.setWindowTitle(MONOA_WINDOW_TITLE)
        self._set_window_size(params)
        self._create_statusbar()
        ui_container = MonoaUI()
        self.setCentralWidget(ui_container)

    def update_window(self, note: Note):
        self.setWindowTitle(f"{MONOA_WINDOW_TITLE} - {note.get_name()}")

    def _create_statusbar(self) -> None:
        ''' Create status bar at the bottom of the main window. '''
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(MONOA_RELEASE)

    def _set_window_size(self, params) -> None:
        ''' Resize app window proportionate to user screen size. '''
        screen_w = params['user_screen_size'].width()
        screen_h = params['user_screen_size'].height()
        window_w = screen_w - 200
        window_h = screen_h - 200
        window_x = screen_w // 2 - window_w // 2
        window_y = screen_h // 2 - window_h // 2
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setMinimumSize(640, 400)

