from datetime import datetime
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt5.QtWidgets import (
    QLabel,         QListWidget,        QMainWindow,
    QStatusBar,     QLineEdit,          QMenu,
    QAction,        QTabWidget,         QDockWidget,
    QFormLayout,    QWidget,            QHBoxLayout,
    QTextEdit,      QToolBar,           QPushButton,
    QVBoxLayout
    )
from services.monoa_service import monoa_service
from entities.snip import Snip
from entities.note import Note
from config import SETTINGS_FILE_PATH
import utils

# Globals
MONOA_WINDOW_TITLE = "MoNoA"
MONOA_RELEASE = "MoNoA Modular Notes App (Version 0.2.0 early bird alpha)"

class MonoaBrowser(QTabWidget):
    '''
    Monoa note editor UI class
    '''
    def __init__(self):
        super().__init__()
        self.addTab(self._createNotesList(), "Notes")
        self.addTab(self._createSnippetsList(), "Snippets")
        self.setMaximumWidth(300)

    def _createNotesList(self):
        note_list_widget = QListWidget()
        note_list_widget.setSpacing(5)
        for note in monoa_service.get_notes():
            list_str = f"{note.get_name()} (#{note.get_id()})\n{note.get_content()[0:40]}"
            note_list_widget.addItem(list_str)
        return note_list_widget

    def _createSnippetsList(self):
        snippet_list_widget = QListWidget()
        snippet_list_widget.setSpacing(5)
        for snippet in monoa_service.get_snips():
            list_str = f"{snippet.get_name()} (#{snippet.get_id()})\n{snippet.get_content()[0:40]}"
            snippet_list_widget.addItem(list_str)
        return snippet_list_widget

class MonoaEditor(QVBoxLayout):
    '''
    Monoa note editor UI class
    '''
    def __init__(self, **params):
        super().__init__()
        self.addWidget(self._createInfoArea())
        self.addWidget(self._createEditArea())

    def _createInfoArea(self):
        return QLabel("Wow")

    def _createEditArea(self):
        monoa_editor = QTextEdit()
        monoa_editor.setAcceptRichText(False)
        return monoa_editor

class MonoaUI(QWidget):
    '''
    Monoa Layout class
    '''
    def __init__(self):
        super().__init__()
        self._createMainLayout()

    def _createMainLayout(self):
        monoa_layout = QHBoxLayout()
        self.setLayout(monoa_layout)
        monoa_layout.addWidget(MonoaBrowser())
        monoa_layout.addLayout(MonoaEditor())

class MonoaMainWindow(QMainWindow):
    '''
    MonoaMainWindow class
    '''
    def __init__(self, parent=None, **params):
        super().__init__(parent)

        # Set main window title and size
        self.setWindowTitle(MONOA_WINDOW_TITLE)
        self._setWindowSize(params)

        # Create top level UI container
        monoa_ui_container = MonoaUI()
        self.setCentralWidget(monoa_ui_container)

        # Create main window status bar
        self._createStatusBar()

    def _createStatusBar(self):
        '''
        Create status bar at the bottom of the main window.
        '''
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(MONOA_RELEASE)
    
    def _setWindowSize(self, params):
        '''
        Resize app window proportionate to user screen size 
        and set minimum size for app window.
        '''
        screen_w = params['user_screen_size'].width()
        screen_h = params['user_screen_size'].height()
        window_w = screen_w - 200
        window_h = screen_h - 200
        window_x = screen_w // 2 - window_w // 2
        window_y = screen_h // 2 - window_h // 2
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setMinimumSize(640, 400)