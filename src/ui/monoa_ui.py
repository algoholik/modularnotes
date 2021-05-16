from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QStatusBar, QWidget, QHBoxLayout)
from entities.snip import Snip
from entities.note import Note

from ui.monoa_browser import MonoaBrowser
from ui.monoa_note_viewer import MonoaNoteViewer

# Globals
MONOA_WINDOW_TITLE = "MoNoA"
MONOA_RELEASE = "MoNoA - Modular Notes App - Version 0.5.0"

class MonoaUI(QWidget):
    '''
    Monoa main UI structure
    '''
    signal_note_selected = QtCore.pyqtSignal(Note)
    signal_note_updated = QtCore.pyqtSignal(Note)
    signal_snip_updated = QtCore.pyqtSignal(Snip)
    def __init__(self):
        super().__init__()

        # Create a Horizontal grid with browser and viewer classes
        self.monoa_layout = QHBoxLayout()
        self.setLayout(self.monoa_layout)
        self.monoa_browser = MonoaBrowser()
        self.monoa_viewer = MonoaNoteViewer()
        self.monoa_layout.addWidget(self.monoa_browser)
        self.monoa_layout.addWidget(self.monoa_viewer)
        self.monoa_layout.setContentsMargins(0,0,0,0)
        self.monoa_layout.setSpacing(0)

        # PyQt Signals handling updates to note currently under editing
        self.monoa_browser.signal_note_selected.connect(self._signal_handler_note_selected)
        self.monoa_viewer.signal_note_updated.connect(self._signal_handler_note_updated)
        self.monoa_viewer.signal_snip_updated.connect(self._signal_handler_snip_updated)

    def _signal_handler_note_selected(self, note):
        self.monoa_viewer.update_note(note)

    def _signal_handler_note_updated(self, note):
        self.monoa_browser.update_active_note(note)
        self.parent().update_window(note)

    def _signal_handler_snip_updated(self, snip):
        self.monoa_browser.update_active_note(snip)
        self.parent().update_window(snip)


class MonoaMainWindow(QMainWindow):
    '''
    MonoaMainWindow class
    '''
    signal_note_selected = QtCore.pyqtSignal(Note)
    signal_note_updated = QtCore.pyqtSignal(Note)
    signal_snip_updated = QtCore.pyqtSignal(Snip)
    def __init__(self, parent=None, **params):
        super().__init__(parent)
        # Set main window title and size
        self.setWindowTitle(MONOA_WINDOW_TITLE)
        self.setContentsMargins(0,0,0,0)
        self._set_window_size(params)
        self._create_statusbar()
        ui_container = MonoaUI()
        self.setCentralWidget(ui_container)

    def update_window(self, note: Note):
        self.setWindowTitle(f"{MONOA_WINDOW_TITLE} - {note.get_title()}")

    def _create_statusbar(self) -> None:
        ''' Create status bar at the bottom of the main window. '''
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(MONOA_RELEASE)

    def _set_window_size(self, params) -> None:
        ''' Resize and position app window proportionate to user screen size. '''
        screen_w = params['user_screen_size'].width()
        screen_h = params['user_screen_size'].height()
        window_w = screen_w - 200
        window_h = screen_h - 200
        window_x = screen_w // 2 - window_w // 2
        window_y = screen_h // 2 - window_h // 2
        self.setGeometry(window_x, window_y, window_w, window_h)
        self.setMinimumSize(640, 400)
