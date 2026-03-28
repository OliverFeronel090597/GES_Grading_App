from PyQt6.QtWidgets            import (
                                QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                                QLabel, QStatusBar, QFrame, QSizePolicy
)
from PyQt6.QtCore               import Qt, QPropertyAnimation, QEasingCurve, QSize, QTimer
from PyQt6.QtGui                import QIcon, QPixmap, QAction
import sys

# Absolute path to the folder containing this script,
from libs.LoginPage                 import PasswordLoginWidget
from libs.DatabaseConnector         import DatabaseConnector
from libs.About                     import AboutDialog
from libs.NotificationManager       import NotificationManager
from libs.Animatedstack             import AnimatedStack
from libs.Globalenentfilter         import GlobalActivityLogger
from libs.Home                      import HomeWidget
from libs.AcademicMasterData        import AcademicMasterData


from libs.GetSchoolYear             import get_current_school_year

# -------------------- MAIN WINDOW --------------------
class GES_StudentGrading(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowTitle("E-Viotrack")
        self.setWindowIcon(QIcon("img/Guintas.png"))
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumWidth(1300) # this is the minimun showable text of the school
        # CREATE TASKBAR | MENU
        self.create_menu()
        self.create_taskbar()

        self.db = DatabaseConnector()
        self.about = AboutDialog(self)

        # NAV STATE
        self.nav_expanded = True
        self.nav_width_expanded = 180
        self.nav_width_collapsed = 75
        self.anim_duration = 500
        self.selected_nav_btn = None
        
        self.icon_size = QSize(40, 40)

        # ICON LOADER
        def load_icon(path, size):
            return QIcon(QPixmap(path).scaled(size, Qt.AspectRatioMode.KeepAspectRatio,
                                             Qt.TransformationMode.SmoothTransformation))

        self.icon_expand = load_icon(
            "img/LeftPanel.png",
            QSize(32, 32)
        )
        
        self.icon_collapse = load_icon(
            "img/RightPanel.png",
            QSize(32, 32)
        )

        self.logo_grading = QPixmap(
            "img/Home.png"
        )
        
        self.logo_admin = QPixmap(
            r"img\grading_200dp_F9DB78_FILL0_wght400_GRAD0_opsz48.png"
        )

        self.logo_build = QPixmap(
            r"img\build_200dp_F9DB78_FILL0_wght400_GRAD0_opsz48.png"
        )

        self.logo_advance = QPixmap(
            "img/Advance.png"
        )

        self.logo_settings = QPixmap(
            "img/Settings.png"
        )

        # ROOT UI
        central = QWidget()
        central.setObjectName("central")
        self.setCentralWidget(central)
        self.root_layout = QHBoxLayout(central)
        self.root_layout.setContentsMargins(0, 0, 0, 0)

        self.notification_manager = NotificationManager(parent=self, position="right")

        # NAV BAR
        self.nav_widget = QWidget()
        self.nav_widget.setObjectName("nav")
        self.nav_widget.setMinimumWidth(self.nav_width_expanded)
        self.nav_widget.setMaximumWidth(self.nav_width_expanded)

        nav_layout = QVBoxLayout(self.nav_widget)
        nav_layout.setContentsMargins(6, 6, 6, 6)

        # TOGGLE BUTTON
        toggle_row = QHBoxLayout()
        toggle_row.addStretch()

        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(44, 44)
        self.toggle_btn.setIcon(self.icon_expand)
        self.toggle_btn.setIconSize(QSize(32, 32))
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_nav)
        self.toggle_btn.setStyleSheet("""
            QPushButton { 
                background: transparent; 
                border: none; }
            QPushButton:hover { 
                background-color: #cc002394; }
        """)

        toggle_row.addWidget(self.toggle_btn)
        nav_layout.addLayout(toggle_row)

        # NAV BUTTONS
        self.btn_home = QPushButton()
        self.btn_grading = QPushButton()
        self.btn_build = QPushButton()
        self.btn_advance = QPushButton()
        self.btn_settings = QPushButton()

        # Setup
        self.setup_nav_button(self.btn_home, self.logo_grading, "Home")
        nav_layout.addWidget(self.btn_home)
        nav_layout.addWidget(self.create_separator("h"))

        self.setup_nav_button(self.btn_grading, self.logo_admin, "Grading")
        nav_layout.addWidget(self.btn_grading)
        nav_layout.addWidget(self.create_separator("h"))

        self.setup_nav_button(self.btn_build, self.logo_build, "Master Data")
        nav_layout.addWidget(self.btn_build)
        nav_layout.addWidget(self.create_separator("h"))

        self.setup_nav_button(self.btn_advance, self.logo_advance, "Advance")
        nav_layout.addWidget(self.btn_advance)
        nav_layout.addWidget(self.create_separator("h"))

        self.setup_nav_button(self.btn_settings, self.logo_settings, "Settings")
        nav_layout.addWidget(self.btn_settings)
        nav_layout.addWidget(self.create_separator("h"))

        nav_layout.addStretch()

        # Fix missing list
        self.nav_buttons = [self.btn_home, self.btn_grading, self.btn_build, self.btn_advance, self.btn_settings]

        # WIDGETS
        self.home_page = HomeWidget(self)
        self.admin_page = AboutDialog()
        self.master_data = AcademicMasterData(self.db, self)
        self.advance_page = AboutDialog()
        self.settings_page = AboutDialog()

        # STACK
        self.stack = AnimatedStack(duration=self.anim_duration)
        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.admin_page)
        self.stack.addWidget(self.master_data)
        self.stack.addWidget(self.advance_page)
        self.stack.addWidget(self.settings_page)

        self.root_layout.addWidget(self.nav_widget)
        self.root_layout.addWidget(self.stack, 1)

        # NAV CLICK HANDLERS
        self.btn_home.clicked.connect(lambda: self.stack.slide_to(0))
        self.btn_grading.clicked.connect(lambda: self.stack.slide_to(1))
        self.btn_build.clicked.connect(lambda: self.stack.slide_to(2))
        self.btn_advance.clicked.connect(lambda: self.stack.slide_to(3))
        self.btn_settings.clicked.connect(lambda: self.stack.slide_to(4))

        QTimer.singleShot(
            2000,
            lambda: self.notification_manager.show_notification(
                f"{QApplication.applicationName()} {QApplication.applicationVersion()}",
                icon_new="SP_MessageBoxInformation"
            )
        )
        #Timer for live reload
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.applySs)
        self.timer.start()

    def applySs(self):
        
        with open("img/Styles.qss", "r") as f:
            self.setStyleSheet(f.read())
           # print("QSSm Updated")

    # -------------------- NOTIFICATION WRAPPER --------------------
    def show_notification(self, message: str = None, icon: str = None):
        """Show a notification using the notification manager."""
        self.notification_manager.show_notification(message, icon_new=icon)

    # -------------------- SEPARATOR --------------------
    def create_separator(self, direction="h"):
        "Line Direction Vertical or Horizontal"
        frame = QFrame()
        frame.setFrameShadow(QFrame.Shadow.Plain)

        if direction.lower().startswith("h"):
            frame.setFrameShape(QFrame.Shape.HLine)
            frame.setFixedHeight(1)
        else:
            frame.setFrameShape(QFrame.Shape.VLine)
            frame.setFixedWidth(1)

        frame.setStyleSheet("background-color: #444;")
        return frame

    # -------------------- NAV BUTTON SETUP --------------------
    def setup_nav_button(self, button: QPushButton, pixmap: QPixmap, text: str):
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        button.setObjectName("navbutton")
        button.setFixedHeight(60)
        button.setToolTip(text)

        # base style for unselected buttons
        default_style = """
            QPushButton {
                color: white;
                background-color: #079fce;
                border: none;
                padding: 5px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #016583;
                border: 1px solid #f53030;
            }
        """
        # selected style
        selected_style = """
            QPushButton {
                color: white;
                background-color: #016583;
                border: 1px solid #f53030;
            }
        """

        button.default_style = default_style
        button.selected_style = selected_style
        button.setStyleSheet(default_style)

        layout = QHBoxLayout(button)
        layout.setContentsMargins(10, 5, 10, 5)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(
            pixmap.scaled(self.icon_size, Qt.AspectRatioMode.KeepAspectRatio,
                          Qt.TransformationMode.SmoothTransformation)
        )
        text_lbl = QLabel(text)
        text_lbl.setStyleSheet("color: white; font-size: 14px;")
        layout.addWidget(icon_lbl)
        layout.addWidget(text_lbl)
        layout.addStretch()

        button.logo_label = icon_lbl
        button.text_label = text_lbl

        # Connect click to selection handler
        button.clicked.connect(lambda checked, b=button: self.select_nav_button(b))

    def select_nav_button(self, button: QPushButton):
        # reset previous
        if self.selected_nav_btn and self.selected_nav_btn != button:
            self.selected_nav_btn.setStyleSheet(self.selected_nav_btn.default_style)

        # set new selected
        button.setStyleSheet(button.selected_style)
        self.selected_nav_btn = button
    # -------------------- FIXED NAV COLLAPSE --------------------
    def toggle_nav(self):
        start = self.nav_widget.width()
        end = self.nav_width_collapsed if self.nav_expanded else self.nav_width_expanded

        # Animate width
        for prop in (b"minimumWidth", b"maximumWidth"):
            anim = QPropertyAnimation(self.nav_widget, prop)
            anim.setDuration(self.anim_duration)
            anim.setStartValue(start)
            anim.setEndValue(end)
            anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
            
            # Update text visibility during animation
            anim.valueChanged.connect(self._update_nav_text_visibility)
            anim.start()
            setattr(self, f"_anim_{prop}", anim)

        self.nav_expanded = not self.nav_expanded
        # switch toggle icon
        self.toggle_btn.setIcon(self.icon_expand if self.nav_expanded else self.icon_collapse)


    def _update_nav_text_visibility(self, value):
        """Show text only if nav is fully expanded, hide otherwise."""
        fully_expanded = value >= self.nav_width_expanded
        for btn in self.nav_buttons:
            btn.text_label.setVisible(fully_expanded)

    # Inside your QMainWindow subclass
    def create_menu(self):
        menubar = self.menuBar()

        # -----------------------
        # File Menu
        # -----------------------
        file_menu = menubar.addMenu("File")

        # About action
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about_dialog)
        file_menu.addAction(about_action)

        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

    # -----------------------
    # Show About Dialog
    # -----------------------
    def show_about_dialog(self):
        dlg = AboutDialog(QApplication.applicationVersion(), self)
        dlg.exec()

        # System Menu
        # menu_title = "System" if not self.version_check(True) else "System 🔴"
        # system_menu = menubar.addMenu(menu_title)
        # check_update_action = QAction("Check for Updates", self)
        # check_update_action.triggered.connect(self.version_check)
        # system_menu.addAction(check_update_action)

        # # Account Menu
        # account_menu = menubar.addMenu("Account")
        # login_action = QAction("Login", self)
        # login_action.triggered.connect(lambda: self.acount_dialog("login"))
        # account_menu.addAction(login_action)

        # change_action = QAction("Change Password", self)
        # change_action.triggered.connect(lambda: self.acount_dialog("change"))
        # account_menu.addAction(change_action)

        # new_action = QAction("New User", self)
        # new_action.triggered.connect(lambda: self.acount_dialog("add"))
        # account_menu.addAction(new_action)

    def create_taskbar(self):
        # Create status bar
        status = QStatusBar()
        status.setObjectName("mainStatusBar")  # Object name for QSS
        status.setContentsMargins(8, 4, 8, 4)

        # LEFT: USER
        self.login_type = QLabel("USER:")
        self.login_type.setObjectName("statusUser")  # QSS target

        # CENTER
        self.connected_device = QLabel(f"SY : {get_current_school_year()}")
        self.connected_device.setObjectName("statusCenter")  # QSS target
        self.connected_device.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # RIGHT: APP VERSION
        version = QApplication.instance().applicationVersion()
        app_name = QApplication.instance().applicationName()
        self.app_name_label = QLabel(f"{app_name} {version}")
        self.app_name_label.setObjectName("statusVersion")  # QSS target

        # Spacers
        left_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        right_spacer = QWidget()
        right_spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        # Add to status bar
        status.addWidget(self.login_type)               # LEFT
        status.addWidget(left_spacer)                   # left spacer
        status.addWidget(self.connected_device)         # CENTER
        status.addWidget(right_spacer)                  # right spacer
        status.addPermanentWidget(self.app_name_label)  # RIGHT
        # USER: USER USER TYPE         | CONNECTED DEVICE |  APP NANE

        # Set status bar
        self.setStatusBar(status)
        

    def print_x(self, xmsg):
        pass
        #print(xmsg)

    # def resizeEvent(self, a0):
    #     print(f"{self.width()}  {self.height()}")
    #     return super().resizeEvent(a0)

# -------------------- RUN --------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationVersion("0.0.0")
    app.setApplicationName("GES Personal Grading")
    event_filter = GlobalActivityLogger()
    app.installEventFilter(event_filter)
    window = GES_StudentGrading()
    window.show()

    logger = GlobalActivityLogger(log_callback=window.print_x, throttle_seconds=1)
    app.installEventFilter(logger)

    sys.exit(app.exec())


# Run
if __name__ == "__main__":
    app = QApplication([])

    win = QWidget()
    layout = QVBoxLayout(win)
    form = PasswordLoginWidget()

    layout.addWidget(form)
    win.setWindowTitle("Login Example")
    win.resize(300, 180)
    win.show()

    app.exec()
