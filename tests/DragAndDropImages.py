import os
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt


class AdviserImageWidget(QWidget):
    SAVE_DIR = "Adviser"
    SAVE_NAME = "adviser"     # extension decided by dropped file
    SIZE = 200                # circle size

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        # Ensure folder exists
        os.makedirs(self.SAVE_DIR, exist_ok=True)

        # UI
        self.label = QLabel("Drop Adviser Image Here")
        self.label.setFixedSize(self.SIZE, self.SIZE)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(
            "QLabel { background: #ddd; border-radius: %dpx; }" % (self.SIZE // 2)
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Load existing saved image if present
        self.load_existing()

    # ============================================================
    # DRAG & DROP
    # ============================================================
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0].toLocalFile().lower()
            if url.endswith((".png", ".jpg", ".jpeg")):
                event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        file_path = event.mimeData().urls()[0].toLocalFile()
        ext = os.path.splitext(file_path)[1].lower()

        save_path = os.path.join(self.SAVE_DIR, f"{self.SAVE_NAME}{ext}")

        # Overwrite existing file
        try:
            # Save to adviser.ext
            img = QImage(file_path)
            img.save(save_path)

            self.show_image(save_path)
        except Exception as e:
            print("Drop error:", e)

    # ============================================================
    # IMAGE HANDLING
    # ============================================================
    def load_existing(self):
        for ext in (".png", ".jpg", ".jpeg"):
            path = os.path.join(self.SAVE_DIR, f"{self.SAVE_NAME}{ext}")
            if os.path.exists(path):
                self.show_image(path)
                return

    def show_image(self, path):
        pix = QPixmap(path).scaled(self.SIZE, self.SIZE, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        # Create circle mask
        circle = QPixmap(self.SIZE, self.SIZE)
        circle.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circle)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(pix))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.SIZE, self.SIZE)
        painter.end()

        # Set to label
        self.label.setPixmap(circle)
        self.label.setText("")  # remove placeholder text


