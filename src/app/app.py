from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QScrollArea,
    QStackedWidget,
    QFileDialog
)
from PySide6.QtGui import (
    QPixmap,
    QFontDatabase,
    QIcon,
    QMouseEvent,
    QShortcut,
    QKeySequence,
    QCursor
)
from PySide6.QtCore import (
    Qt,
    Signal
)
from enum import Enum
from datetime import datetime
import sys
import os
import resources_rc
import base64
import json
import sqlite3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cards import CardMainFrame
from basetab import BaseTab
from editor import EditorWindow
from dialogs import (
    ExitDialog,
    OverTabDialog,
    FileOpenDialog,
    FileNotFoundDialog
)

def base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class WindowStaticValue(Enum):
    WIDTH: int = 1000
    HEIGHT: int = 650
    LEFT: int = 100
    TOP: int = 50
    TITLE: str = "Imject"
    
    ROOT_PATH: str = base_path()
    CSS_PATH: str = os.path.join(ROOT_PATH, "styles")
    ICONS_PATH: str = os.path.join(ROOT_PATH, "assets", "icons")
    FONTS_PATH: str = os.path.join(ROOT_PATH, "resources", "fonts")
    DATABASE_PATH: str = os.path.join(ROOT_PATH, "databases", "files.db")
    
class HorizontalScrollArea(QScrollArea):
    def wheelEvent(self, event):
        # Only scroll horizontally with the wheel
        if event.angleDelta().y() != 0:
            # Scroll horizontally by the vertical delta
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - event.angleDelta().y()
            )
            event.accept()
        else:
            super().wheelEvent(event)
            
class ClickableWidget(QWidget):
    clicked: Signal = Signal()

    def __init__(self):
        super().__init__()
        
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            
class CustomDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def getKeyFromValue(self, value):
        for key, value_ in self.items():
            if value_ == value:
                return key

class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        self.tabs_list: list[BaseTab] = []
        self.editors_list: list[EditorWindow] = []
        self.cards_dict: CustomDict = CustomDict()
        self.imp_cards_dict: CustomDict = CustomDict()
        self.file_path_list: list[str] = []
        
        self.init_window()
        
    def init_window(self) -> None:
        self.logo_path: str = WindowStaticValue.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        self.setGeometry(WindowStaticValue.LEFT.value, WindowStaticValue.TOP.value, WindowStaticValue.WIDTH.value, WindowStaticValue.HEIGHT.value)
        self.setWindowTitle(WindowStaticValue.TITLE.value)
        self.setObjectName("main-window")
        
        self.STYLESHEET: str = ""
        
        with open(f"{WindowStaticValue.CSS_PATH.value + r"\mainwindow.qss"}", "r") as file_:
            self.STYLESHEET += file_.read()
            
        self.setStyleSheet(self.STYLESHEET)          
            
        # add font
        QFontDatabase.addApplicationFont(WindowStaticValue.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(WindowStaticValue.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.init_window_widgets()

    def init_window_widgets(self) -> None:
        # Whole layout
        self.main_layout: QVBoxLayout = QVBoxLayout()
        
        # Top frame for tab buttons
        self.tab_frame: QWidget = QWidget()
        self.tab_frame.setObjectName("tab-frame")
        
        # stack widget
        self.stack_widget: QStackedWidget = QStackedWidget()
        
        # Main frame 
        self.main_frame: QWidget = QWidget()
        self.main_frame.setObjectName("main-frame")
        
        self.stack_widget.addWidget(self.main_frame)
        
        # Cards frame
        self.files_frame: QWidget = QWidget()
        
        # Horizontal layout for cards and side frame
        self.side_layout: QHBoxLayout = QHBoxLayout()
        
        # Vertical layout for side frame
        self.side_frame_layout: QVBoxLayout = QVBoxLayout()
        self.side_frame_layout.setContentsMargins(0,0,0,0)
        self.side_frame_layout.setSpacing(0)

        # Side frame
        self.side_frame: QWidget = QWidget()
        self.side_frame.setObjectName("side-frame")

        # Button frames
        self.new_button_frame: ClickableWidget = ClickableWidget()
        self.new_button_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        self.open_button_frame: ClickableWidget = ClickableWidget()
        self.open_button_frame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Button frame layouts
        self.new_button_frame_layout: QHBoxLayout = QHBoxLayout()
        self.new_button_frame_layout.setContentsMargins(0,0,0,0)
        self.new_button_frame_layout.setSpacing(0)
        
        self.open_button_frame_layout: QHBoxLayout = QHBoxLayout()
        self.open_button_frame_layout.setContentsMargins(0,0,0,0)
        self.open_button_frame_layout.setSpacing(0)
        
        # new button
        self.new_btn_icon_label: QLabel = QLabel()
        self.new_btn_icon_label.setObjectName("img")
        self.new_btn_icon = QPixmap(f"{WindowStaticValue.ICONS_PATH.value + r"\new_icon.png"}") 
        self.new_btn_icon_label.setPixmap(self.new_btn_icon)
        self.new_btn_icon_label.setProperty("class", "icon-label")
        
        self.new_btn_label: QLabel = QLabel(text="New")
        self.new_btn_label.setProperty("class", "btn-label")
        
        self.new_button_frame_layout.addWidget(self.new_btn_icon_label)
        self.new_button_frame_layout.addWidget(self.new_btn_label)
        
        # open button
        self.open_btn_icon_label: QLabel = QLabel()
        self.open_btn_icon = QPixmap(f"{WindowStaticValue.ICONS_PATH.value + r"\open_icon.png"}")
        self.open_btn_icon_label.setPixmap(self.open_btn_icon)
        self.open_btn_icon_label.setProperty("class", "icon-label")
        self.open_btn_icon_label.setStyleSheet("""
                                                margin-top: 25px;
                                               """)
        
        self.open_btn_label: QLabel = QLabel(text="Open")
        self.open_btn_label.setProperty("class", "btn-label")
        self.open_btn_label.setStyleSheet("""
                                            margin-top: 25px;
                                         """)
        
        self.open_button_frame_layout.addWidget(self.open_btn_icon_label)
        self.open_button_frame_layout.addWidget(self.open_btn_label)
        
        self.new_button_frame.clicked.connect(self.new_file)
        self.open_button_frame.clicked.connect(self.open_file)
        
        # shortcut
        self.new_file_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.new_file_shortcut.activated.connect(self.new_file)

        self.open_file_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.open_file_shortcut.activated.connect(self.open_file)
        
        # setting layouts
        self.side_frame.setLayout(self.side_frame_layout)

        self.side_frame_layout.addWidget(self.new_button_frame)
        self.side_frame_layout.addWidget(self.open_button_frame)
        
        # setting layouts
        self.new_button_frame.setLayout(self.new_button_frame_layout)
        self.open_button_frame.setLayout(self.open_button_frame_layout)
        
        # ------------------ CARDS SECTION -----------------
        # scroll area for cards
        self.scroll_area_imp: QScrollArea = HorizontalScrollArea()
        self.scroll_area_imp.setProperty("cssClass", "scroll-area")
        self.scroll_area_imp.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area_imp.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area_imp.setWidgetResizable(True)
        
        self.scroll_area_file: QScrollArea = HorizontalScrollArea()
        self.scroll_area_file.setProperty("cssClass", "scroll-area")
        self.scroll_area_file.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area_file.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area_file.setWidgetResizable(True)
        
        # vboxlayout
        self.file_section_layout: QVBoxLayout = QVBoxLayout()
        self.file_section_layout.setContentsMargins(0,0,0,20)
        self.file_section_layout.setSpacing(0)
        
        # layout set
        self.files_frame.setLayout(self.file_section_layout)
        
        # header label - 'IMPORTANT'
        self.important_label: QLabel = QLabel("Important")
        self.important_label.setProperty("class", "header-label")
        
        # CARDS 
        self.cards_widget: QWidget = QWidget()
        self.cards_widget.setObjectName("cards-widget")
        self.scroll_area_imp.setWidget(self.cards_widget)
        
        self.card_layout: QHBoxLayout = QHBoxLayout()
        self.card_layout.setContentsMargins(32,30,32,0)
        self.card_layout.setSpacing(30)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.cards_widget.setLayout(self.card_layout)
        
        self.files_label: QLabel = QLabel("Files")
        self.files_label.setProperty("class", "header-label")
        
        self.card_layout2: QHBoxLayout = QHBoxLayout()
        self.card_layout2.setContentsMargins(32,30,32,0)
        self.card_layout2.setSpacing(30)
        self.card_layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.cards_widget2: QWidget = QWidget()
        self.cards_widget2.setObjectName("cards-widget")

        self.scroll_area_file.setWidget(self.cards_widget2)
        
        self.cards_widget2.setLayout(self.card_layout2)
        
        # widgets add
        self.file_section_layout.addWidget(self.important_label)
        self.file_section_layout.addWidget(self.scroll_area_imp)
        self.file_section_layout.addWidget(self.files_label)
        self.file_section_layout.addWidget(self.scroll_area_file)
        # ----------------------------------------------------
        
        # ---------------------------------- tabs ---------------------------------
        # tab layout
        self.tab_layout: QHBoxLayout = QHBoxLayout()
        self.tab_layout.setContentsMargins(15,0,0,0)
        self.tab_layout.setSpacing(0)
        self.tab_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tab_frame.setLayout(self.tab_layout)
        
        # home icon
        self.icon_home_path: str = f"{WindowStaticValue.ICONS_PATH.value + r'\home_icon.png'}"
        self.home_button: QPushButton = QPushButton()
        self.home_button.setObjectName("home-button")
        self.home_button.setIcon(QIcon(self.icon_home_path))
        
        self.home_button.clicked.connect(self.open_home)
        
        # tabs container
        self.tabs_container: QWidget = QWidget()
        self.tabs_container.setObjectName("tabs-container")
        
        self.tabs_container_layout: QHBoxLayout = QHBoxLayout(self.tabs_container)
        self.tabs_container_layout.setContentsMargins(15,0,0,0)
        self.tabs_container_layout.setSpacing(0)
        self.tabs_container_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.tabs_container.setLayout(self.tabs_container_layout)
                
        # adding widgets to tab layout
        self.tab_layout.addWidget(self.home_button)
        self.tab_layout.addWidget(self.tabs_container)

        # -------------------------------------------------------------------------        
        # Side layout adding widgets
        self.side_layout.addWidget(self.side_frame)
        self.side_layout.addWidget(self.files_frame)
        self.side_layout.setContentsMargins(0,0,0,0)
        self.side_layout.setSpacing(0)
        
        # adding layout to mainframe
        self.main_frame.setLayout(self.side_layout)

        self.main_layout.addWidget(self.tab_frame)
        self.main_layout.addWidget(self.stack_widget)
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)

        self.setLayout(self.main_layout)
        
        self.side_frame_layout.addStretch()
        
        self.get_startup_data()
        self.handle_cmd_argument()
        
    def new_file(self) -> None:
        if len(self.tabs_list) >= 7:
            self.overtab_dialog: OverTabDialog = OverTabDialog()
            self.overtab_dialog.show()

            return
        
        for tabs in self.tabs_list:
            tabs.change_state(False)
        
        tab: BaseTab = BaseTab(title="untitled", active=True, active_beside=None)
        self.tabs_list.append(tab)
        self.tabs_container_layout.addWidget(tab)

        # index_: int = self.tabs_list.index(tab)
        tab.clicked.connect(self.change_tab)
        tab.close.connect(self.close_tab_)

        editor: EditorWindow = EditorWindow()
        self.editors_list.append(editor)
        self.stack_widget.addWidget(editor)
        
        editor.saveFile.connect(self.change_tab_name)
        editor.editFile.connect(self.change_tab_name)
        editor.saveSignal.connect(self.save_data_db)

        index: int = self.editors_list.index(editor)
        self.stack_widget.setCurrentIndex(index+1)
        
        try:
            prev_tab: BaseTab = self.tabs_list[index-1]
        except:
            pass
        else:
            prev_tab.change_active_beside("left")
            
        try:
            next_tab: BaseTab = self.tabs_list[index+1]
        except:
            pass
        else:
            next_tab.change_active_beside("right")
        
    def open_home(self) -> None:
        self.stack_widget.setCurrentIndex(0)
        for tabs in self.tabs_list:
            tabs.change_active_beside(None)
            tabs.change_state(False)
        
    def change_tab(self, object_: BaseTab) -> None:
        index: int = self.tabs_list.index(object_)
        for tabs in self.tabs_list:
            tabs.change_state(False)
            
        try:
            prev_tab: BaseTab = self.tabs_list[index-1]
        except:
            pass
        else:
            prev_tab.change_active_beside("left")
            
        try:
            next_tab: BaseTab = self.tabs_list[index+1]
        except:
            pass
        else:
            next_tab.change_active_beside("right")
            
        tab: BaseTab = self.tabs_list[index]
        tab.change_state(True)

        self.stack_widget.setCurrentIndex(index+1)
        
    def open_file(self) -> None:
        if len(self.tabs_list) >= 7:
            self.overtab_dialog: OverTabDialog = OverTabDialog()
            self.overtab_dialog.show()

            return
        
        file_dialog: QFileDialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Imject file (*.imject)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        
        if not file_dialog.exec():
            return
        
        file_path: str = file_dialog.selectedFiles()[0]
        file_name: str = os.path.basename(file_path)
        
        self.open_file_(file_path=file_path, file_name=file_name)

    def open_file_(self, file_path: str, file_name: str, card: CardMainFrame|None = None) -> None:
        if len(self.tabs_list) >= 7:
            self.overtab_dialog: OverTabDialog = OverTabDialog()
            self.overtab_dialog.show()

            return
        
        if file_path in self.file_path_list:
            self.fileopen_dialog: FileOpenDialog = FileOpenDialog()
            self.fileopen_dialog.show()

            return
        
        try:
            with open(file_path, "r") as file_:
                global encoded_data
                encoded_data = file_.read()
        except FileNotFoundError:
            self.filenotfound_dialog: FileNotFoundDialog = FileNotFoundDialog()
            self.filenotfound_dialog.show()

            if card is not None:
                self.filenotfound_dialog.removeSignal.connect(lambda: self.remove_card(card))
            
            return
        except Exception: 
            pass
        
        json_data: str = base64.b64decode(encoded_data.encode("utf-8")).decode("utf-8")
        data = json.loads(json_data)
        
        for tabs in self.tabs_list:
            tabs.change_state(False)
        
        tab: BaseTab = BaseTab(title=f"{file_name}", active=True, active_beside=None, file_path=file_path)
        self.tabs_list.append(tab)
        self.tabs_container_layout.addWidget(tab)

        tab.clicked.connect(self.change_tab)
        tab.close.connect(self.close_tab_)

        editor: EditorWindow = EditorWindow()
        self.editors_list.append(editor)
        self.stack_widget.addWidget(editor)
        
        editor.change_file_path(file_path)
        
        editor.saveFile.connect(self.change_tab_name)
        editor.editFile.connect(self.change_tab_name)
        editor.saveSignal.connect(self.save_data_db)
        
        editor.open_file_(data)
        
        self.file_path_list.append(file_path)

        index: int = self.editors_list.index(editor)
        self.stack_widget.setCurrentIndex(index+1)
        
        try:
            prev_tab: BaseTab = self.tabs_list[index-1]
        except:
            pass
        else:
            prev_tab.change_active_beside("left")
            
        try:
            next_tab: BaseTab = self.tabs_list[index+1]
        except:
            pass
        else:
            next_tab.change_active_beside("right")
            
    def close_tab_(self, object_: BaseTab):
        index: int = self.tabs_list.index(object_)
        tab: BaseTab = self.tabs_list[index]
        widget: EditorWindow = self.editors_list[index]
        
        tab_name: str = tab.get_tab_name()
        if tab_name == "untitled" or tab_name[0] == "*":
            self.exitdialog: ExitDialog = ExitDialog()
            self.exitdialog.show()
            self.exitdialog.exitSignal.connect(lambda: self.func_close_tab(tab=tab, widget=widget, index=index))
        else:
            self.func_close_tab(tab=tab, widget=widget, index=index)      
            
        file_path: str | None = tab.return_file_path()

        if file_path != None:
            try:
                self.file_path_list.remove(file_path)
            except Exception:
                pass
            
    def func_close_tab(self, tab: BaseTab, widget: EditorWindow, index: int) -> None:
        self.tabs_container_layout.removeWidget(tab)
        tab.deleteLater()
            
        self.tabs_list.pop(index)
        self.editors_list.pop(index)
            
        self.stack_widget.removeWidget(widget)
        widget.deleteLater()
            
        self.open_home()
        
    def change_tab_name(self, object_: EditorWindow, file_path: str, status: str) -> None:
        index: int = self.editors_list.index(object_)
        tab: BaseTab = self.tabs_list[index]
        file_name: str = os.path.basename(file_path)
        tab.change_file_path(file_path=file_path)

        if status == "saved":
            tab.change_title_label(file_name)
        elif status == "edited" and file_path != "":
            tab.change_title_label(f"*{file_name}")
        elif status == "edited" and file_path == "":
            tab.change_title_label("untitled")
            
    def save_data_db(self, file_path: str, exist: str) -> None:
        connection = sqlite3.connect(WindowStaticValue.DATABASE_PATH.value)
        
        cursor = connection.cursor()
        
        file_name: str = os.path.basename(file_path)
        date: str = datetime.today().strftime('%d-%m-%Y')
        
        if exist == "new":        
            data: tuple = (file_path, file_name, date, date)
            
            query = """--sql
            INSERT INTO FILES (filepath, filename, created, edited) VALUES (?, ?, ?, ?);           
            """
            
            cursor.execute(query, data)

            connection.commit()
            
            created: str = f"Created: {date}"
            edited: str = f"Last edited: {date}"
            
            file_card: CardMainFrame = CardMainFrame(property_="files", file_name=file_name, created=created, edited=edited)
            self.card_layout2.addWidget(file_card)
            
            file_card.clicked.connect(self.file_card_clicked)
            file_card.fileMarkedImp.connect(self.mark_file_as_imp)
            file_card.removeFile.connect(self.remove_file_from_db)
            
            self.cards_dict[file_path] = file_card
            
        elif exist == "exist":
            data: tuple = (date, file_path)            

            query = """--sql
            UPDATE FILES           
            SET edited = ?
            WHERE filepath = ?;
            """
            
            cursor.execute(query, data)
            
            card: CardMainFrame = self.cards_dict.get(file_path)
            if card is not None:
                text: str = f"Last edited: {date}"
                card.set_edited_label(text=text)
            
            connection.commit()
            
            query = """--sql
            UPDATE IMPFILES           
            SET edited = ?
            WHERE filepath = ?;
            """
            
            cursor.execute(query, data)
            
            card_: CardMainFrame = self.imp_cards_dict.get(file_path)
            if card_ is not None:
                text: str = f"Last edited: {date}"
                card_.set_edited_label(text=text)

            connection.commit()
            
        connection.close()
        
        if file_path not in self.file_path_list:
            self.file_path_list.append(file_path)
        
    def get_startup_data(self) -> None:
        connection = sqlite3.connect(WindowStaticValue.DATABASE_PATH.value)
        
        cursor = connection.cursor()
        
        query = """--sql
        SELECT * FROM FILES;
        """
        
        cursor.execute(query)
        rows: list = cursor.fetchall()

        for data in rows:
            created: str = f"Created: {data[3]}"
            edited: str = f"Last edited: {data[4]}"
            file_name: str = data[2]
            file_path: str = data[1]

            file_card: CardMainFrame = CardMainFrame(property_="files", file_name=file_name, created=created, edited=edited)
            self.card_layout2.addWidget(file_card)
            
            file_card.clicked.connect(self.file_card_clicked)
            file_card.fileMarkedImp.connect(self.mark_file_as_imp)
            file_card.removeFile.connect(self.remove_file_from_db)

            self.cards_dict[file_path] = file_card
            
        query = """--sql
        SELECT * FROM IMPFILES;
        """
        
        cursor.execute(query)
        rows: list = cursor.fetchall()

        for data in rows:
            created: str = f"Created: {data[3]}"
            edited: str = f"Last edited: {data[4]}"
            file_name: str = data[2]
            file_path: str = data[1]

            file_card: CardMainFrame = CardMainFrame(property_="important", file_name=file_name, created=created, edited=edited)
            self.card_layout.addWidget(file_card)
            
            file_card.clicked.connect(self.file_card_clicked)
            file_card.removeFile.connect(self.remove_file_from_db)

            self.imp_cards_dict[file_path] = file_card
        
        connection.close()
        
    def file_card_clicked(self, object_: CardMainFrame, property_: str) -> None:
        file_path: str = ""
        file_name: str = ""

        if property_ == "important":
            file_path = self.imp_cards_dict.getKeyFromValue(object_)
            file_name = os.path.basename(file_path)
        elif property_ == "files":
            file_path = self.cards_dict.getKeyFromValue(object_)
            file_name = os.path.basename(file_path)

        self.open_file_(file_path=file_path, file_name=file_name, card=object_)
        
    def mark_file_as_imp(self, object_: CardMainFrame) -> None:
        connection = sqlite3.connect(WindowStaticValue.DATABASE_PATH.value)
        
        cursor = connection.cursor()
        
        query: str = """--sql
        SELECT * FROM FILES WHERE filepath = ? ;
        """
        
        file_path: str = self.cards_dict.getKeyFromValue(object_)
        
        cursor.execute(query, (file_path,))
        row: tuple = cursor.fetchall()[0]

        file_name: str = row[2]
        created: str = row[3]
        edited: str = row[4]

        query: str = """--sql
        INSERT INTO IMPFILES (filepath, filename, created, edited) VALUES (?, ?, ?, ?);
        """
        
        cursor.execute(query, (file_path, file_name, created, edited))
        connection.commit()

        created = f"Created: {created}"
        edited = f"Last edited: {edited}"

        file_card: CardMainFrame = CardMainFrame(property_="important", file_name=file_name, created=created, edited=edited)
        self.card_layout.addWidget(file_card)
            
        file_card.clicked.connect(self.file_card_clicked)
        file_card.removeFile.connect(self.remove_file_from_db)
            
        self.imp_cards_dict[file_path] = file_card
        
        connection.close()

    def remove_file_from_db(self, object_: CardMainFrame) -> None:
        property_: str = object_.property
        
        connection = sqlite3.connect(WindowStaticValue.DATABASE_PATH.value)
        cursor = connection.cursor()
        
        if property_ == "files":
            file_path: str = self.cards_dict.getKeyFromValue(object_)   
            
            query = """--sql
            DELETE FROM FILES WHERE filepath = ? ;
            """
            
            cursor.execute(query, (file_path, ))
            
            self.card_layout2.removeWidget(object_)
            object_.setParent(None)
            object_.deleteLater()
            
            connection.commit()

        elif property_ == "important":
            file_path: str = self.imp_cards_dict.getKeyFromValue(object_)   
            
            query = """--sql
            DELETE FROM IMPFILES WHERE filepath = ? ;
            """
            
            cursor.execute(query, (file_path, ))
            
            self.card_layout.removeWidget(object_)
            object_.setParent(None)
            object_.deleteLater()
            
            connection.commit()
            
        connection.close()
        
    def handle_cmd_argument(self) -> None:
        file_path: str = ""
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            try:
                file_name: str = os.path.basename(file_path)
                self.open_file_(file_path=file_path, file_name=file_name)
                    
            except Exception as e:
                print(e)
                
    def remove_card(self, card: CardMainFrame) -> None:
        self.remove_file_from_db(object_=card)
        self.filenotfound_dialog.close()