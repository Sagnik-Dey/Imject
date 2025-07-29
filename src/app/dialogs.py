from PySide6.QtWidgets import (
    QLabel, 
    QDialog,
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
    QWidget, 
    QApplication
)
from PySide6.QtGui import (
    QFontDatabase, 
    Qt,
    QIcon
)
from PySide6.QtCore import (
    Signal
)
import os
import sys
from enum import Enum

def base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class DialogStaticValues(Enum):
    ROOT_PATH: str = base_path()
    CSS_PATH: str = os.path.join(ROOT_PATH, "styles")
    ICONS_PATH: str = os.path.join(ROOT_PATH, "assets", "icons")
    FONTS_PATH: str = os.path.join(ROOT_PATH, "resources", "fonts")

class ExitDialog(QDialog):
    exitSignal: Signal = Signal()

    def __init__(self):
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.init_window()

    def init_window(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
        self.label: QLabel = QLabel("File is not saved")
        self.label.setObjectName("exitdialog-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_widget: QWidget = QWidget()
        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(50,0,50,0)
        self.buttons_layout.setSpacing(20)
        self.btn_widget.setLayout(self.buttons_layout)
        
        self.cancel_btn: QPushButton = QPushButton("Cancel")
        self.cancel_btn.setProperty("cssClass", "dialog-btn")
        self.exit_btn: QPushButton = QPushButton("Exit")
        self.exit_btn.setProperty("cssClass", "dialog-btn")
        
        self.cancel_btn.clicked.connect(lambda: self.close())
        self.exit_btn.clicked.connect(self.exit_clicked)

        self.buttons_layout.addWidget(self.cancel_btn)
        self.buttons_layout.addWidget(self.exit_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
    
    def exit_clicked(self) -> None:
        self.exitSignal.emit()
        self.close()
        
class NoLayoutDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
                
        self.init_window()
        
    def init_window(self) -> None:
        self.setObjectName("nolayout-dialog")
        
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text: str = "No layout is selected.\nSelect a layout before adding images"
        self.label: QLabel = QLabel(text=text)
        self.label.setObjectName("nolayout-dialog-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_widget: QWidget = QWidget()
        self.btn_widget_layout: QHBoxLayout = QHBoxLayout()
        self.btn_widget_layout.setContentsMargins(0,0,0,0)
        self.btn_widget_layout.setSpacing(0)
        self.btn_widget.setLayout(self.btn_widget_layout)
        self.btn_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ok_btn: QPushButton = QPushButton("Ok")
        self.ok_btn.setProperty("cssClass", "dialog-btn")
        self.ok_btn.setObjectName("nolayout-dialog-btn")
        
        self.ok_btn.clicked.connect(lambda: self.close())

        self.btn_widget_layout.addWidget(self.ok_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
        
class NoImagesDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.init_window()
        
    def init_window(self) -> None:
        self.setObjectName("noimages-dialog")
        
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text: str = "No images are uploaded.\nUpload images first"
        self.label: QLabel = QLabel(text=text)
        self.label.setObjectName("noimages-dialog-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_widget: QWidget = QWidget()
        self.btn_widget_layout: QHBoxLayout = QHBoxLayout()
        self.btn_widget_layout.setContentsMargins(0,0,0,0)
        self.btn_widget_layout.setSpacing(0)
        self.btn_widget.setLayout(self.btn_widget_layout)
        self.btn_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ok_btn: QPushButton = QPushButton("Ok")
        self.ok_btn.setProperty("cssClass", "dialog-btn")
        self.ok_btn.setObjectName("noimages-dialog-btn")
        
        self.ok_btn.clicked.connect(lambda: self.close())

        self.btn_widget_layout.addWidget(self.ok_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
        
class ProgressDoneDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.init_window()
        
    def init_window(self) -> None:
        self.setObjectName("progress-done-dialog")
        
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text: str = "PDF exported successfully"
        self.label: QLabel = QLabel(text=text)
        self.label.setObjectName("progress-done-dialog-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_widget: QWidget = QWidget()
        self.btn_widget_layout: QHBoxLayout = QHBoxLayout()
        self.btn_widget_layout.setContentsMargins(0,0,0,0)
        self.btn_widget_layout.setSpacing(0)
        self.btn_widget.setLayout(self.btn_widget_layout)
        self.btn_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ok_btn: QPushButton = QPushButton("Ok")
        self.ok_btn.setProperty("cssClass", "dialog-btn")
        self.ok_btn.setObjectName("progress-done-dialog-btn")
        
        self.ok_btn.clicked.connect(lambda: self.close())

        self.btn_widget_layout.addWidget(self.ok_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
        
class OverTabDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.init_window()
        
    def init_window(self) -> None:
        self.setObjectName("overtab-dialog")
        
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text: str = "Can't open more than 7 tabs"
        self.label: QLabel = QLabel(text=text)
        self.label.setObjectName("overtab-dialog-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_widget: QWidget = QWidget()
        self.btn_widget_layout: QHBoxLayout = QHBoxLayout()
        self.btn_widget_layout.setContentsMargins(0,0,0,0)
        self.btn_widget_layout.setSpacing(0)
        self.btn_widget.setLayout(self.btn_widget_layout)
        self.btn_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ok_btn: QPushButton = QPushButton("Ok")
        self.ok_btn.setProperty("cssClass", "dialog-btn")
        self.ok_btn.setObjectName("overtab-dialog-btn")
        
        self.ok_btn.clicked.connect(lambda: self.close())

        self.btn_widget_layout.addWidget(self.ok_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
        
class FileOpenDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.init_window()
        
    def init_window(self) -> None:
        self.setObjectName("fileopen-dialog")
        
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        text: str = "File is already open in another tab"
        self.label: QLabel = QLabel(text=text)
        self.label.setObjectName("fileopen-dialog-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.btn_widget: QWidget = QWidget()
        self.btn_widget_layout: QHBoxLayout = QHBoxLayout()
        self.btn_widget_layout.setContentsMargins(0,0,0,0)
        self.btn_widget_layout.setSpacing(0)
        self.btn_widget.setLayout(self.btn_widget_layout)
        self.btn_widget_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.ok_btn: QPushButton = QPushButton("Ok")
        self.ok_btn.setProperty("cssClass", "dialog-btn")
        self.ok_btn.setObjectName("fileopen-dialog-btn")
        
        self.ok_btn.clicked.connect(lambda: self.close())

        self.btn_widget_layout.addWidget(self.ok_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
        
class FileNotFoundDialog(QDialog):
    removeSignal: Signal = Signal()

    def __init__(self):
        super().__init__()
        
        with open(f"{DialogStaticValues.CSS_PATH.value + r"\dialogs.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(DialogStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.setWindowModality(Qt.WindowModality.WindowModal)      
        self.setWindowTitle("Imject")
        
        self.logo_path: str = DialogStaticValues.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.init_window()

    def init_window(self) -> None:
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
        self.label: QLabel = QLabel("No such file or directory exist")
        self.label.setObjectName("filenotfound-label")
        self.label.setProperty("cssClass", "dialog-label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_widget: QWidget = QWidget()
        self.buttons_layout: QHBoxLayout = QHBoxLayout()
        self.buttons_layout.setContentsMargins(50,0,50,0)
        self.buttons_layout.setSpacing(20)
        self.btn_widget.setLayout(self.buttons_layout)
        
        self.ok_btn: QPushButton = QPushButton("Ok")
        self.ok_btn.setProperty("cssClass", "dialog-btn")
        self.remove_btn: QPushButton = QPushButton("Remove")
        self.remove_btn.setProperty("cssClass", "dialog-btn")
        
        self.ok_btn.clicked.connect(lambda: self.close())
        self.remove_btn.clicked.connect(self.remove_clicked)

        self.buttons_layout.addWidget(self.ok_btn)
        self.buttons_layout.addWidget(self.remove_btn)
        
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.btn_widget)

        self.setLayout(self.main_layout)
    
    def remove_clicked(self) -> None:
        self.removeSignal.emit()
        
if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    app.setStyle("Fusion")
    window: ExitDialog = ExitDialog()
    window.show()
    sys.exit(app.exec())