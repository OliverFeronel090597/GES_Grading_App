from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt


class TitleCaseLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textEdited.connect(self._to_title_case)
        self._updating = False

    def _to_title_case(self, text):
        if self._updating:
            return

        # Title-case WITHOUT removing spaces
        normalized = []
        capitalize_next = True

        for ch in text:
            if capitalize_next and ch.isalpha():
                normalized.append(ch.upper())
                capitalize_next = False
            else:
                normalized.append(ch)
                capitalize_next = (ch == " ")

        normalized = "".join(normalized)

        # Update text safely
        if normalized != text:
            cursor_pos = self.cursorPosition()
            self._updating = True
            self.setText(normalized)
            self.setCursorPosition(cursor_pos)
            self._updating = False