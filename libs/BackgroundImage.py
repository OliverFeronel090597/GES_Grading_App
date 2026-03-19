from PyQt6.QtWidgets import QWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt, QSize


class PixmapBgWidget(QWidget):
    def __init__(self, opacity=1, parent=None):
        super().__init__(parent)
        self.bg = QPixmap("img/Guintas.png")
        self.opacity = opacity # 10%

        # Make sure it expands like a normal page
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(0, 0)

        # Make Qt treat it like a normal background (no shrink)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

    def sizeHint(self):
        # Force the background widget to follow parent's full size
        if self.parent():
            return self.parent().size()
        return QSize(800, 600)

    def minimumSizeHint(self):
        return self.sizeHint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        painter.drawPixmap(self.rect(), self.bg)
