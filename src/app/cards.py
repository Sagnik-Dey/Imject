from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QLabel,
    QApplication,
    QMenu
)
from PySide6.QtGui import (
    QFontDatabase,
    QAction
)
from PySide6.QtCore import (
    Qt,
    Signal,
    QPoint
)
from enum import Enum
import os
import sys

def base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CardsStaticValues(Enum):
    WIDTH: int = 200
    HEIGHT: int = 200
    LEFT: int = 100
    TOP: int = 50
    
    ROOT_PATH: str = base_path()
    CSS_PATH: str = os.path.join(ROOT_PATH, r"styles\cards.qss")
    ICONS_PATH: str = os.path.join(ROOT_PATH, "assets", "icons")
    FONTS_PATH: str = os.path.join(ROOT_PATH, "resources", "fonts")
    
class CardMainFrame(QWidget):
    clicked: Signal = Signal(object, str)
    fileMarkedImp: Signal = Signal(object)
    removeFile: Signal = Signal(object)

    def __init__(self, property_: str, file_name: str, created: str, edited: str) -> None:
        super().__init__()

        self.property: str = property_
        self.file_name: str = file_name
        self.created: str = created
        self.edited: str = edited
        
        self.init_window()

    def init_window(self) -> None:         
        # # add font
        QFontDatabase.addApplicationFont(CardsStaticValues.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(CardsStaticValues.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        # self.setObjectName("card-main-frame")
        self.setProperty("cssClass", "card-main-frame")
        self.setProperty("impProperty", self.property)
        
        with open(CardsStaticValues.CSS_PATH.value, "r") as file_:
            self.setStyleSheet(file_.read())
            
        self.setAttribute(Qt.WA_StyledBackground, True) 
        self.init_window_widgets()

    def init_window_widgets(self) -> None:
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        
        # main layout
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)
        
        # File name label
        self.file_name_label: QLabel = QLabel(text=self.file_name)
        self.file_name_label.setProperty("cssClass", "file-name-label")
        self.file_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Date created label
        self.date_created_label: QLabel = QLabel(text=self.created)
        self.date_created_label.setProperty("cssClass", "date-proj-label")
        self.date_created_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # File name label
        self.last_edited_label: QLabel = QLabel(text=self.edited)
        self.last_edited_label.setProperty("cssClass", "date-proj-label")
        self.last_edited_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.file_name_label)
        self.main_layout.addWidget(self.date_created_label)
        self.main_layout.addWidget(self.last_edited_label)
        
        self.main_layout.addStretch()
        
        self.setLayout(self.main_layout)
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self, self.property)
            
    def show_context_menu(self, pos: QPoint) -> None:
        menu: QMenu = QMenu()
        remove_action: QAction | None = None
        action: QAction | None = None
        
        with open(CardsStaticValues.CSS_PATH.value, "r") as file_:
            menu.setStyleSheet(file_.read())
            
        if self.property == "important":
            remove_action = menu.addAction("Remove")  

            action: QAction = menu.exec(self.mapToGlobal(pos))
        else:
            mark_imp_action: QAction = menu.addAction("Mark as important") 
            remove_action = menu.addAction("Remove")  

            action: QAction = menu.exec(self.mapToGlobal(pos))
            
            if action == mark_imp_action:
                self.fileMarkedImp.emit(self)
                
        if action == remove_action:
            self.removeFile.emit(self)
        
    def set_edited_label(self, text: str) -> None:
        self.last_edited_label.setText(text)
        
if __name__ == "__main__":
    appy = QApplication(sys.argv)

    win = CardMainFrame()
    win.show()

    appy.exec()