from datetime import datetime
from PyQt5 import QtCore
from PyQt5.QtCore import (Qt, QMimeData, QSize)
from PyQt5.QtGui import (
    QDrag, QPixmap, QPainter, QTextCursor, QFontMetrics, QFontDatabase
)
from PyQt5.QtWidgets import (
    QLabel, QLineEdit, QHBoxLayout, QTextEdit, QPushButton, QVBoxLayout, QDialog, QFrame, QWidget,
)
from services.monoa_service import monoa_service
from entities.snip import Snip
from entities.note import Note
from ui.monoa_text_edit import MonoaTextEdit
from ui.monoa_styles import CSS

class MonoaSnipEditor(QFrame):
    '''Custom QFrame class to contain snip editor.'''
    signal_snip_updated = QtCore.pyqtSignal(Snip)
    def __init__(self, snip: Snip):
        super().__init__()
        self.setMinimumHeight(24)
        self.sizeHint()
        self.setContentsMargins(0,0,0,0)
        self.setObjectName("Snip")
        self.setStyleSheet(CSS.get("snip_area"))
        self.snip = snip

        self.snip_editor = MonoaTextEdit()
        self.snip_editor.setMinimumLines(1)
        self.snip_editor.setObjectName("TaskDescription")
        self.snip_editor.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.snip_editor.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.snip_editor.setAcceptRichText(False)

        font_fixed = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        font_fixed.setPointSize(14)

        self.snip_editor.setFont(font_fixed)
        self.snip_editor.setPlaceholderText("Empty snip")
        self.snip_editor.setPlainText(self.snip.get_content())
        self.snip_editor.setTabStopDistance(
            QFontMetrics(self.snip_editor.font()).horizontalAdvance(' ') * 4
        )
        self.snip_editor.moveCursor(QTextCursor.End)

        #btn_edit_snip = QPushButton("Edit")  # QIcon("images/three_dots.png"), None
        #btn_edit_snip.setMaximumSize(30, 30)
        #btn_edit_snip.clicked.connect(self.specifyTaskInfo)
        #delete_task_button.clicked.connect(self.deleteTaskItem)

        self.label_snip_id = QLabel(f"Snip #{str(self.snip.get_id())}")
        self.label_snip_id.setObjectName("SnipId")
        self.label_snip_id.setStyleSheet(CSS.get("snip_id_label"))
        self.label_snip_id.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_snip_modified = QLabel(f"{str(self.snip.get_modified())}")
        self.label_snip_modified.setObjectName("SnipModified")
        self.label_snip_modified.setStyleSheet(CSS.get("snip_modified_label"))
        self.label_snip_modified.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.snip_toolbar = QWidget()
        self.snip_toolbar_hbox = QHBoxLayout()
        self.snip_toolbar_hbox.addWidget(self.label_snip_id)
        self.snip_toolbar_hbox.addWidget(self.label_snip_modified)
        self.snip_toolbar.setLayout(self.snip_toolbar_hbox)
        self.snip_toolbar_hbox.setContentsMargins(0,0,0,0)
        self.snip_toolbar_hbox.setSpacing(0)

        snip_vbox = QVBoxLayout()
        snip_vbox.addWidget(self.snip_toolbar)
        snip_vbox.addWidget(self.snip_editor)
        snip_vbox.setContentsMargins(0,0,0,0)
        snip_vbox.setSpacing(0)
        self.setLayout(snip_vbox)

        self.snip_editor.textChanged.connect(self._autosave_snip)

    def update_snip(self, snip: Snip) -> None:
        ''' Loads MonoaEditor with a new Snip object. '''
        self.snip = snip
        self._update_editor()

    def _update_editor(self) -> None:
        self.label_snip_id.setText(f"Snip #{str(self.snip.get_id())}")
        self.snip_editor.setText(self.snip.get_content())

    def _autosave_snip(self) -> None:
        self.snip.set_content(self.snip_editor.toPlainText())
        self._update_browser()

    def _update_browser(self) -> None:
        self.signal_snip_updated.emit(self.snip)
        monoa_service.update_snip(self.snip)
        print("snip autosave")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        drag = QDrag(self)
        mime_data = QMimeData()
        drag.setMimeData(mime_data)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec(Qt.MoveAction)
