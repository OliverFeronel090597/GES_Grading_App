from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import Qt
import sys

class PixmapBgWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.bg = QPixmap("img/Guintas.png")
        self.opacity = 0.1  # max opacity

    def paintEvent(self, event):
        painter = QPainter(self)

        # Set opacity for the background image
        painter.setOpacity(self.opacity)

        # Auto-stretch to widget size
        painter.drawPixmap(self.rect(), self.bg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PixmapBgWidget()
    w.resize(800, 500)  # now auto-stretches
    w.show()
    sys.exit(app.exec())
