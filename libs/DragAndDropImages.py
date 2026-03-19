from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QImage, QPainter, QBrush, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt
import os


class DragAndDropImage(QWidget):
    SAVE_DIR = "Images"  # single folder for all images

    def __init__(self, logo_type: str = "adviser", size: int = 200, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.max_size = size
        self.logo_type = logo_type
        self.save_name = logo_type  # filename = type name

        # Ensure folder exists
        os.makedirs(self.SAVE_DIR, exist_ok=True)

        # UI
        self.label = QLabel(f"Drop {self.logo_type.capitalize()} Image Here")
        self.label.setObjectName("dragImage")
        self.label.setFixedSize(self.max_size, self.max_size)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Use pixels for border-radius
        self.label.setStyleSheet(
            f"QLabel#dragImage {{ background: #ddd; border-radius: {self.max_size // 2}px; border: 1px solid black; }}"
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Load existing saved image if present
        self.load_existing()

    # ---------------- DRAG & DROP ----------------
    def dragEnterEvent(self, event: QDragEnterEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile().lower()
            if file_path.endswith((".png", ".jpg", ".jpeg")):
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if not urls or not urls[0].isLocalFile():
            return
        file_path = urls[0].toLocalFile()
        ext = os.path.splitext(file_path)[1].lower()
        save_path = os.path.join(self.SAVE_DIR, f"{self.save_name}{ext}")

        try:
            img = QImage(file_path)
            img.save(save_path)  # overwrite if exists
            self.show_image(save_path)
        except Exception as e:
            print(f"Drop error for {self.logo_type}: {e}")

    # ---------------- IMAGE HANDLING ----------------
    def load_existing(self):
        for ext in (".png", ".jpg", ".jpeg"):
            path = os.path.join(self.SAVE_DIR, f"{self.save_name}{ext}")
            if os.path.exists(path):
                self.show_image(path)
                return

    def show_image(self, path):
        pix = QPixmap(path).scaled(
            self.max_size,
            self.max_size,
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )

        # Circular mask
        circle = QPixmap(self.max_size, self.max_size)
        circle.fill(Qt.GlobalColor.transparent)

        painter = QPainter(circle)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(pix))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.max_size, self.max_size)
        painter.end()

        self.label.setPixmap(circle)
        self.label.setText("")  # remove placeholder text
