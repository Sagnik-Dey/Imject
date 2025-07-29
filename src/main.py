from PySide6.QtWidgets import (
    QApplication
)
from PySide6.QtGui import QFontDatabase
from app import app
import os
import sys

def base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def start_app() -> None:
    ROOT_PATH: str = base_path()
    CSS_PATH: str = os.path.join(ROOT_PATH, "styles")
    FONTS_PATH: str = os.path.join(ROOT_PATH, "resources", "fonts")
    STYLESHEET: str = ""
        
    with open(f"{CSS_PATH + r"\mainwindow.qss"}", "r") as file_:
            STYLESHEET += file_.read()
        
    application: QApplication = QApplication(sys.argv)
    window: app.MainWindow = app.MainWindow()

    application.setStyleSheet(STYLESHEET)  
    application.setStyle("Fusion")
    
    QFontDatabase.addApplicationFont(FONTS_PATH + r"\Montserrat-Regular.ttf")
    QFontDatabase.addApplicationFont(FONTS_PATH + r"\Montserrat-Bold.ttf")
    
    window.show()

    application.exec()

if __name__ == "__main__":
    start_app()