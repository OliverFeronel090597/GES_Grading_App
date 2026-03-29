import sys
from PyQt6.QtWidgets import QSplashScreen, QApplication, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QTimer

class SplashScreen(QSplashScreen):
    """
    A frameless, transparent splash screen with fade-in and fade-out animation.

    This splash screen:
      • displays a QPixmap on a transparent background
      • fades in on startup
      • stays visible for 3 seconds
      • fades out automatically
      • shows the main window after finishing the fade-out

    Parameters
    ----------
    pixmap : QPixmap
        The image displayed on the splash screen.
    parent : QWidget, optional
        The main application window to show after the splash closes.

    Attributes
    ----------
    fade_in_anim : QPropertyAnimation
        Animation controlling the fade-in opacity transition.
    fade_out_anim : QPropertyAnimation
        Animation controlling the fade-out opacity transition.
    parent_x : QWidget
        Reference to the main window that will be shown after the splash.
    """

    def __init__(self, pixmap: QPixmap, parent: QWidget = None):
        super().__init__(pixmap, Qt.WindowType.FramelessWindowHint)
        self.parent_x = parent
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Keep animation references
        self.fade_in_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out_anim = QPropertyAnimation(self, b"windowOpacity")    # <-- fixed typo

        self.show()
        self.fade_in()

    def fade_in(self):
        self.setWindowOpacity(0.0)
        self.fade_in_anim.setDuration(800)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(1.0)
        self.fade_in_anim.start()
        QTimer.singleShot(3000, self.fade_out)

    def fade_out(self):
        self.fade_out_anim.setDuration(800)
        self.fade_out_anim.setStartValue(1.0)
        self.fade_out_anim.setEndValue(0.0)
        self.fade_out_anim.finished.connect(self.finish_splash)
        self.fade_out_anim.start()

    def finish_splash(self):
        self.close()
        self.parent_x.show()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()

#     try:
#         pixmap = QPixmap("img/Banner.png")
#         if pixmap.isNull():
#             raise FileNotFoundError("Cannot load img/Banner.png")
#     except Exception as e:
#         print("Error loading splash image:", e)
#         sys.exit(1)

#     splash = SplashScreen(pixmap, window)
#     sys.exit(app.exec())
