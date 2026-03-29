from PyQt6.QtWidgets import QMessageBox, QWidget

class MessageBox:
    """
    Wrapper for PyQt6 QMessageBox with all common functions.
    """

    def __init__(self, parent: QWidget = None):
        self.parent = parent

    # -----------------------------
    # Basic Information
    # -----------------------------
    def info(self, title: str, message: str, detailed: str = None):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        if detailed:
            msg.setDetailedText(detailed)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg.exec()

    # -----------------------------
    # Warning
    # -----------------------------
    def warning(self, title: str, message: str, detailed: str = None):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        if detailed:
            msg.setDetailedText(detailed)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg.exec()

    # -----------------------------
    # Critical / Error
    # -----------------------------
    def critical(self, title: str, message: str, detailed: str = None):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        if detailed:
            msg.setDetailedText(detailed)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        return msg.exec()

    # -----------------------------
    # Question / Yes-No
    # -----------------------------
    def question(self, title: str, message: str, yes_text="Yes", no_text="No"):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(message)
        yes = msg.addButton(yes_text, QMessageBox.ButtonRole.YesRole)
        no = msg.addButton(no_text, QMessageBox.ButtonRole.NoRole)
        msg.setDefaultButton(yes)
        msg.exec()
        return msg.clickedButton() == yes

    # -----------------------------
    # Ok-Cancel
    # -----------------------------
    def ok_cancel(self, title: str, message: str):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Question)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        result = msg.exec()
        return result == QMessageBox.StandardButton.Ok

    # -----------------------------
    # Retry-Cancel
    # -----------------------------
    def retry_cancel(self, title: str, message: str):
        msg = QMessageBox(self.parent)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStandardButtons(QMessageBox.StandardButton.Retry | QMessageBox.StandardButton.Cancel)
        result = msg.exec()
        return result == QMessageBox.StandardButton.Retry

    # -----------------------------
    # Custom buttons
    # -----------------------------
    def custom(self, title: str, message: str, buttons: list):
        """
        buttons: list of tuples [(text, role), ...]
        role: QMessageBox.ButtonRole enum
        """
        msg = QMessageBox(self.parent)
        msg.setWindowTitle(title)
        msg.setText(message)
        for text, role in buttons:
            msg.addButton(text, role)
        msg.exec()
        return msg.clickedButton().text()
    

# # Create wrapper
# mb = MessageBox(self)  # self = parent QWidget

# # Information
# mb.info("Info", "This is an info message")

# # Warning
# mb.warning("Warning", "Something might be wrong!")

# # Critical
# mb.critical("Error", "This is critical!")

# # Question Yes/No
# if mb.question("Confirm", "Do you want to continue?"):
#     print("User clicked Yes")
# else:
#     print("User clicked No")

# # Ok/Cancel
# if mb.ok_cancel("Save", "Do you want to save changes?"):
#     print("Ok clicked")

# # Retry/Cancel
# if mb.retry_cancel("Network", "Retry connecting?"):
#     print("Retrying...")

# # Custom buttons
# btn = mb.custom(
#     "Custom", 
#     "Choose an option", 
#     [("Option 1", QMessageBox.ButtonRole.ActionRole),
#      ("Option 2", QMessageBox.ButtonRole.ActionRole)]
# )
# print("Clicked:", btn)