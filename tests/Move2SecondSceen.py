from PyQt6.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        # Widgets
        self.label = QLabel("Enter Text:")
        self.text_input = QLineEdit()
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.button = QPushButton("Submit")
        self.button.clicked.connect(self.on_button_click)

        # Add widgets to layout
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.text_input)
        main_layout.addWidget(self.button)
        main_layout.addWidget(self.text_display)

    def on_button_click(self):
        entered_text = self.text_input.text()
        self.text_display.append(f"You entered: {entered_text}")

def move_to_second_screen(window:QMainWindow):
    screens = QApplication.screens()
    if len(screens) < 2:
        print("Only one monitor detected.")
        return
    
    screen = screens[1]  # second monitor
    print(screen.name())
    geo = screen.availableGeometry()
    print(geo)
    window.move(geo.center() - window.rect().center())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    move_to_second_screen(window)
    sys.exit(app.exec())