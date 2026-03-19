from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QApplication, QSizePolicy
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSlot
import sys


class CollapsibleWidget(QWidget):
    def __init__(self, title: str, content: str, parent=None):
        super().__init__(parent)

        self.toggle_button = QPushButton(title)
        self.toggle_button.setCheckable(True)
        self.toggle_button.setChecked(False)
        self.toggle_button.setStyleSheet(
            "QPushButton { text-align: left; font-weight: bold; }"
        )
        self.toggle_button.clicked.connect(self.on_toggle)

        # Content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 5, 10, 5)
        self.content_label = QLabel(content)
        self.content_label.setWordWrap(True)
        self.content_layout.addWidget(self.content_label)

        # Set initial size
        self.content_widget.setMaximumHeight(0)
        self.content_widget.setMinimumHeight(0)

        # Animation for collapse/expand
        self.animation = QPropertyAnimation(self.content_widget, b"maximumHeight")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Main layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.toggle_button)
        layout.addWidget(self.content_widget)

    @pyqtSlot()
    def on_toggle(self):
        if self.toggle_button.isChecked():
            # Expand to content height
            self.content_widget.setMaximumHeight(0)
            self.animation.setStartValue(0)
            self.animation.setEndValue(self.content_label.sizeHint().height() + 20)
        else:
            # Collapse
            self.animation.setStartValue(self.content_widget.height())
            self.animation.setEndValue(0)
        self.animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    details_text = (
        "Paaralang Elementarya ng Guintas, or Guintas Elementary School, "
        "is a public primary school located in Barangay Guintas, Leganes, Iloilo, Philippines. "
        "Serving the local community for decades, the school provides education for Grades 1 through 6 "
        "and is part of the DepEd Schools Division of Iloilo. "
        "The school has a close connection with the community, with an active alumni association "
        "that supports scholarships, reunions, and community projects. "
        "Established around the mid-20th century, Guintas Elementary has grown alongside the barangay, "
        "which has expanded from a small settlement to a vibrant community of over 2,000 residents. "
        "The school remains an important institution in Guintas, fostering education and community engagement, "
        "and contributing to the social infrastructure of Leganes."
    )

    window = QWidget()
    layout = QVBoxLayout(window)

    collapsible = CollapsibleWidget("Guintas Elementary School Details", details_text)
    layout.addWidget(collapsible)

    layout.addStretch()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec())
