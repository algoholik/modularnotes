from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
QLineEdit, QWidget, QHBoxLayout, QPushButton, QVBoxLayout, QScrollArea, QFileDialog,
QMessageBox
)
from services.monoa_service import monoa_service
from entities.snip import Snip
from entities.note import Note
from ui.monoa_snip_editor import MonoaSnipEditor
from ui.monoa_styles import CSS

class MonoaNoteContainer(QWidget):
    signal_note_updated = QtCore.pyqtSignal(Note)
    signal_snip_updated = QtCore.pyqtSignal(Snip)
    def __init__(self, note: Note):
        super().__init__()
        self.setObjectName("NoteContainer")
        self.setAcceptDrops(True)
        self.note = note

        # Path variable for export dialog
        self.path = None

        self.signal_snip_updated.connect(self._update_note_from_snip)

        # Header area with note title and add snip button
        # Note title editor
        self.note_title = QLineEdit(self.note.get_title())
        self.note_title.setStyleSheet(CSS.get("note_title"))
        self.note_title.setPlaceholderText("Untitled")
        self.note_title.textChanged.connect(self._autosave_note)
        # add snip button
        self.btn_add_snip = QPushButton("Add Snip")
        self.btn_add_snip.clicked.connect(self.create_snip)
        self.btn_export = QPushButton("Export Note...")
        self.btn_export.clicked.connect(self._file_export)
        # Header area layout
        self.note_header_hbox = QHBoxLayout()
        # Header area widget
        self.note_header_area = QWidget()
        self.note_header_area.setObjectName("HeaderArea")
        self.note_header_area.setLayout(self.note_header_hbox)
        self.note_header_hbox.setContentsMargins(0,0,0,0)
        self.note_header_hbox.setSpacing(0)
        self.note_header_hbox.addWidget(self.note_title)
        self.note_header_hbox.addWidget(self.btn_add_snip)
        self.note_header_hbox.addSpacing(5)
        self.note_header_hbox.addWidget(self.btn_export)

        self.snips_container_frame = QWidget()
        self.snips_container_frame.setObjectName("ContainerFrame")


        self.snips_v_box = QVBoxLayout()
        self.snips_v_box.setDirection(QVBoxLayout.TopToBottom)
        self.snips_container_frame.setLayout(self.snips_v_box)
        self.snips_v_box.setContentsMargins(0,0,0,0)
        self.snips_v_box.setSpacing(0)

        # Make it scroll baby
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.snips_container_frame)

        # Main layout for container class
        self.container_v_box = QVBoxLayout()
        self.container_v_box.setSpacing(0)
        self.container_v_box.setAlignment(Qt.AlignTop)
        self.container_v_box.addWidget(self.note_header_area)
        self.container_v_box.addWidget(self.scroll_area)
        self.container_v_box.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.container_v_box)

        # Load note viewer with snips assigned to it
        self._populate_note_contents()

    def create_snip(self):
        new_snip = MonoaSnipEditor(monoa_service.create_snip_inside_note(self.note.get_id()))
        new_snip_pos = self.snips_v_box.count() + 1
        self.snips_v_box.insertWidget(new_snip_pos, new_snip, 0)

    def update_note(self, note: Note) -> None:
        self.note = note
        self.note_title.setText(self.note.get_title())
        self._update_note_view()

    def _update_note_from_snip(self, snip: Snip) -> None:
        self.signal_snip_updated.emit(self.snip)

    def _populate_note_contents(self) -> None:
        for snip in self.note.get_contents():
            new_snip = MonoaSnipEditor(snip)
            new_snip_pos = self.snips_v_box.count() + 1
            self.snips_v_box.insertWidget(new_snip_pos, new_snip, 0)

    def _init_note_view(self):
        for snip in reversed(range(self.snips_v_box.count())):
            snip_widget = self.snips_v_box.takeAt(snip).widget()
            if snip_widget is not None:
                snip_widget.close()

    def _autosave_note(self) -> None:
        self.note.set_title(self.note_title.text())
        self.signal_note_updated.emit(self.note)
        monoa_service.update_note(self.note)
        #self._update_browser()

    def _update_browser(self) -> None:
        pass
        #self.signal_note_updated.emit(self.note)
        #monoa_service.update_note(self.note)

    def _update_note_view(self) -> None:
        self._init_note_view()
        self._populate_note_contents()

    def dragEnterEvent(self, event):
        """Accept the dragging event onto the widget."""
        event.setAccepted(True)

    def dropEvent(self, event):
        event.setDropAction(Qt.MoveAction)
        drag_source = event.source()
        if drag_source not in self.children():
            event.setAccepted(True)
            self.snips_v_box.addWidget(drag_source)
        else:
            event.setAccepted(False)

    def _file_export(self):
        selected_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export note as text file",
            f"{self.note.get_title()}.txt",
            "Text documents (*.txt); All files (*.*)"
        )
        if not selected_path: return
        self._export_to_path(selected_path)

    def _export_to_path(self, path):
        text_contents = monoa_service.render_textfile_contents(self.note.get_id())
        print(text_contents)
        try:
            with open(path, 'w') as file:
                file.write(text_contents)
        except Exception as error:
            self._export_error_msg(str(error))
        else:
            self.path = path

    def _export_error_msg(self, errormsg: str):
        error_popup = QMessageBox()
        error_popup.setIcon(QMessageBox.Information)
        error_popup.setWindowTitle("MoNoA - Error while exporting")
        error_popup.setText(f"MoNoA got the following error:\n\n{errormsg}")
        error_popup.setStandardButtons(QMessageBox.Ok)
        btn_clicked = error_popup.exec()
        # Just close the dialog if OK button is clicked
        if btn_clicked == QMessageBox.Ok: pass
