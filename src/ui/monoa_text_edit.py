from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import (QFontMetrics, QColor, QTextFormat)
from PyQt5.QtCore import (Qt, QSize)

# Globals
ROW_HIGHLIGHT_COLOR = QColor(Qt.yellow).lighter(150)

class MonoaTextEdit(QTextEdit):
    def __init__(self, parent = None):
        super(MonoaTextEdit, self).__init__(parent)
        self.textChanged.connect(lambda: self.updateGeometry())
        self.cursorPositionChanged.connect(self.highlight_active_row)

    def highlight_active_row(self):
        ''' Creates a secondary cursor that highlights the full row where the
        primary cursor is. '''
        selections = []
        sel = QTextEdit.ExtraSelection()
        sel.format.setBackground(ROW_HIGHLIGHT_COLOR)
        sel.format.setProperty(QTextFormat.FullWidthSelection, True)
        sel.cursor = self.textCursor()
        sel.cursor.clearSelection()
        selections.append(sel)
        self.setExtraSelections(selections)

    def set_min_rows(self, num_rows):
        ''' Overwrite PyQt setMinimumLines to respond to '''
        self.setMinimumSize(self.minimumSize().width(), self.rows_to_widget_height(num_rows))

    def hasHeightForWidth(self):
        ''' Overwrite PyQt hasHeightForWidth function to split snip edit areas evenly'''
        return True

    def heightForWidth(self, width):
        ''' Overwrite PyQthgeightForWidth function to split snip edit areas evenly'''
        margins = self.contentsMargins()
        if width >= margins.left() + margins.right():
            document_width = width - margins.left() - margins.right()
        else:
            document_width = 0
        document = self.document().clone()
        document.setTextWidth(document_width)
        return margins.top() + document.size().height() + margins.bottom()

    def sizeHint(self):
        ''' Overwrite PyQt sizeHint. '''
        original_hint = super(MonoaTextEdit, self).sizeHint()
        return QSize(original_hint.width(), self.heightForWidth(original_hint.width()))

    def rows_to_widget_height(self, line_count):
        assert line_count >= 0
        widget_margins = self.contentsMargins()
        document_margin = self.document().documentMargin()
        font_metrics = QFontMetrics(self.document().defaultFont())
        return (
            widget_margins.top() +
            document_margin +
            max(line_count, 1) * (font_metrics.height()+2) +
            self.document().documentMargin() +
            widget_margins.bottom()
        )
