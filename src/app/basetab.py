from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PySide6.QtGui import (
    Qt,
    QIcon,
    QFontDatabase
)
from PySide6.QtCore import (
    QSize,
    Signal
)
from enum import Enum
import os
import sys

def base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class WindowStaticValue(Enum):
    ROOT_PATH: str = base_path()
    CSS_PATH: str = os.path.join(ROOT_PATH, "styles")
    ICONS_PATH: str = os.path.join(ROOT_PATH, "assets", "icons")
    FONTS_PATH: str = os.path.join(ROOT_PATH, "resources", "fonts")

class BaseTab(QFrame):
    clicked: Signal = Signal(object)
    close: Signal = Signal(object)

    def __init__(self, title:str="Project 1", active:bool=False, active_beside:str|None =None, file_path: str|None = None) -> None:
        super().__init__()
        
        self.title_name: str = title
        self.active: bool = active
        self.active_beside: str = active_beside  # "left", "right", or None
        self.file_path: str | None = file_path
        
        with open(f"{WindowStaticValue.CSS_PATH.value + r"\basetab.qss"}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        self.setProperty("cssClass", "baseTab")
        self.setProperty("active", str(self.active))
        self.setProperty("active-beside", str(self.active_beside))
        
        QFontDatabase.addApplicationFont(WindowStaticValue.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(WindowStaticValue.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.init_widgets()
        # self.setFixedHeight(36)  # optional: match your design

    def init_widgets(self) -> None:
        # Layout
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 5, 10, 5)
        self.layout.setSpacing(8)

        # Left icon (edit/pencil)
        self.icon_label: QLabel = QLabel()
        self.icon_path: str = f"{WindowStaticValue.ICONS_PATH.value + r'\tab_icon.png'}" 
        self.icon_label.setPixmap(QIcon(self.icon_path).pixmap(10, 10)) 
        self.layout.addWidget(self.icon_label)

        # Tab title
        self.title_label: QLabel = QLabel(self.title_name)
        self.title_label.setProperty("cssClass", "tab-title")
        self.layout.addWidget(self.title_label)

        # Spacer
        self.layout.addStretch()

        # Close button (icon)
        self.close_button: QPushButton = QPushButton()
        self.close_button.setProperty("cssClass", "close-tab-buttons")
        self.icon_path_close: str = f"{WindowStaticValue.ICONS_PATH.value + r'\close_tab_icon.png'}"
        self.close_button.setIcon(QIcon(self.icon_path_close))  # <-- Replace with your icon path
        self.close_button.setIconSize(QSize(14, 14))
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setToolTip("Close tab")

        self.close_button.clicked.connect(self.close_tab)

        self.layout.addWidget(self.close_button)

    def change_state(self, state: bool) -> None:
        self.active = state
        self.setProperty("active", str(self.active))        
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        
    def change_active_beside(self, side: str | None) -> None:
        self.active_beside = side
        self.setProperty("active-beside", str(self.active_beside))
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()
        
    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self)
             
    def close_tab(self) -> None:
        self.close.emit(self)
    
    def change_title_label(self, value: str) -> None:
        self.title_label.setText(value)
        
    def get_tab_name(self) -> str:
        return self.title_label.text()
    
    def return_file_path(self) -> str|None:
        return self.file_path
    
    def change_file_path(self, file_path: str) -> None:
        self.file_path = file_path