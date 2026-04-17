from PyQt6.QtWidgets                    import QApplication, QMainWindow
from layouts.Globalenentfilter          import GlobalActivityLogger
from MainWindow                         import GES_StudentGrading
import sys

def move_to_second_screen(window:QMainWindow):
    screens = QApplication.screens()
    if len(screens) < 2:
        print("Only one monitor detected.")
        return
    
    screen = screens[1]  # second monitor
    geo = screen.availableGeometry()
    window.move(geo.center() - window.rect().center())

# -------------------- RUN --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationVersion("0.0.0")
    app.setApplicationName("GES Personal Grading")
    event_filter = GlobalActivityLogger()
    app.installEventFilter(event_filter)
    window = GES_StudentGrading()
    window.show()
    move_to_second_screen(window)

    # logger = GlobalActivityLogger(log_callback=window.print_x, throttle_seconds=1)
    # app.installEventFilter(logger)

    sys.exit(app.exec())
