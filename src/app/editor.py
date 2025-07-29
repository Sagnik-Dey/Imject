from PySide6.QtWidgets import (
    QApplication,
    QWidget, 
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QGridLayout,
    QLabel,
    QSizePolicy,
    QMenu,
    QRadioButton,
    QButtonGroup,
    QMessageBox,
    QProgressDialog
)
from PySide6.QtCore import (
    Qt,
    QSize,
    QObject,
    Signal,
    QPoint,
    QTimer
)
from PySide6.QtGui import (
    QIcon,
    QFontDatabase,
    QPixmap,
    QAction,
    QPainter,
    QPageSize,
    QShortcut,
    QKeySequence
)
from PySide6.QtPrintSupport import QPrinter
from enum import Enum
import sys
import os
import json
import base64

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from dialogs import (
    NoLayoutDialog,
    NoImagesDialog,
    ProgressDoneDialog    
)

def base_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class EditorStaticValue(Enum):
    WIDTH = 950
    HEIGHT = 650
    LEFT = 100
    TOP = 50
    
    ROOT_PATH: str = base_path()
    CSS_PATH: str = os.path.join(ROOT_PATH, "styles")
    ICONS_PATH: str = os.path.join(ROOT_PATH, "assets", "icons")
    FONTS_PATH: str = os.path.join(ROOT_PATH, "resources", "fonts")
    
class ImagesWindow(QWidget):
    def __init__(self, images_path_list: list) -> None:
        super().__init__()
        
        self.LEFT: int = 100
        self.TOP: int = 70
        self.WIDTH: int = 850
        self.HEIGHT: int = 600
        self.TITLE: str = "Imject"
        
        self.images_path_list: list = images_path_list
        self.current_index: int = 0
        
        self.init_window()
    
    def init_window(self) -> None:
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)
        
        with open(f"{EditorStaticValue.CSS_PATH.value + r'\editor.qss'}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        self.logo_path: str = EditorStaticValue.ICONS_PATH.value + r"\logo.png"
        self.setWindowIcon(QIcon(self.logo_path))
        
        QFontDatabase.addApplicationFont(EditorStaticValue.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(EditorStaticValue.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.init_window_widgets()

    def init_window_widgets(self) -> None:
        # main layout
        self.setObjectName("images-window")
        
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)
        
        self.title_bar: QWidget = QWidget()
        self.title_bar.setObjectName("title-bar")
        self.title_bar.setProperty("cssClass", "bar")
        
        self.title_bar_layout: QHBoxLayout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(10, 0, 10, 0)    
        self.title_bar.setLayout(self.title_bar_layout)    
        
        self.file_title_label: QLabel = QLabel(self.images_path_list[self.current_index])
        self.file_title_label.setObjectName("file-title-label")
        self.file_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.title_bar_layout.addWidget(self.file_title_label)

        self.image_frame: QWidget = QWidget()
        self.image_frame.setObjectName("image-frame")
        self.image_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.image_path: str = self.images_path_list[self.current_index]
        self.image_label: QLabel = QLabel()
        
        pixmap: QPixmap = QPixmap(self.image_path)
        pixmap = pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # image label
        self.image_frame_layout: QVBoxLayout = QVBoxLayout()
        self.image_frame.setLayout(self.image_frame_layout)
        
        self.image_frame_layout.addWidget(self.image_label)
        
        # controls bar widget
        self.controls_bar: QWidget = QWidget()
        self.controls_bar.setObjectName("controls-bar")
        self.controls_bar.setProperty("cssClass", "bar")
        
        self.left_arrow_icon_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "left_arrow.png")
        self.left_arrow_disabled_icon_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "left_arrow_disabled.png")
        
        self.previous_button: QPushButton = QPushButton()
        self.previous_button.setProperty("cssClass", "image-slide-buttons")
        
        # icon 
        icon: QIcon = QIcon()
        icon.addPixmap(QPixmap(self.left_arrow_icon_path), QIcon.Mode.Normal, QIcon.State.On)
        icon.addPixmap(QPixmap(self.left_arrow_disabled_icon_path), QIcon.Mode.Disabled, QIcon.State.On)
        
        self.previous_button.setIcon(icon)
        self.previous_button.setIconSize(QSize(17, 17))
        self.previous_button.setToolTip("Previous Image")
        self.previous_button.setEnabled(False)
        
        self.right_arrow_icon_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "right_arrow.png")
        self.right_arrow_disabled_icon_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "right_arrow_disabled.png")
        self.next_button: QPushButton = QPushButton()
        self.next_button.setProperty("cssClass", "image-slide-buttons")
        
        icon_: QIcon = QIcon()
        icon_.addPixmap(QPixmap(self.right_arrow_icon_path), QIcon.Mode.Normal, QIcon.State.On)
        icon_.addPixmap(QPixmap(self.right_arrow_disabled_icon_path), QIcon.Mode.Disabled, QIcon.State.On)
        
        self.next_button.setIcon(icon_)
        self.next_button.setIconSize(QSize(17, 17))
        self.next_button.setToolTip("Next Image")
        
        self.controls_bar_layout: QHBoxLayout = QHBoxLayout()
        self.controls_bar_layout.setContentsMargins(25, 0, 25, 0)
        self.controls_bar.setLayout(self.controls_bar_layout)
        
        self.controls_bar_layout.addWidget(self.previous_button)
        self.controls_bar_layout.addStretch()
        self.controls_bar_layout.addWidget(self.next_button)
        
        self.previous_button.clicked.connect(lambda: self.change_image("previous"))
        self.next_button.clicked.connect(lambda: self.change_image("next"))
        
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addWidget(self.image_frame)
        self.main_layout.addWidget(self.controls_bar)
        
    def change_image(self, direction: str) -> None:
        if direction == "next":
            self.current_index += 1
        elif direction == "previous":
            self.current_index -= 1
        
        if self.current_index == 0:
            self.previous_button.setEnabled(False)

        elif self.current_index == len(self.images_path_list) - 1:
            self.next_button.setEnabled(False)
            
        if self.current_index != 0:
            self.previous_button.setEnabled(True)
        if self.current_index != (len(self.images_path_list) - 1):
            self.next_button.setEnabled(True)
        
        self.file_title_label.setText(self.images_path_list[self.current_index])
        
        pixmap: QPixmap = QPixmap(self.images_path_list[self.current_index])
        pixmap = pixmap.scaled(600, 600, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

class EditorWindow(QWidget):
    saveFile: Signal = Signal(object, str, str)
    editFile: Signal = Signal(object, str, str)
    saveSignal: Signal = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()

        self.images_paths_list: list[str] = []
        self.active_layout: str | None = None  # Default layout
        self.page_width: int = 744
        self.page_height: int = 1052
        self.a4_pages_list: list[QWidget] = []
        self.a4_pages_layout_list: list[QGridLayout] = []
        self.current_file: str | None = None

        self.setGeometry(
            EditorStaticValue.LEFT.value,
            EditorStaticValue.TOP.value,
            EditorStaticValue.WIDTH.value,
            EditorStaticValue.HEIGHT.value
        )
        
        with open(f"{EditorStaticValue.CSS_PATH.value + r'\editor.qss'}", "r") as file_:
            self.setStyleSheet(file_.read())
        
        self.setObjectName("editor-window")
        self.setAttribute(Qt.WA_StyledBackground, True)
        
        # add font
        QFontDatabase.addApplicationFont(EditorStaticValue.FONTS_PATH.value + r"\Montserrat-Regular.ttf")
        QFontDatabase.addApplicationFont(EditorStaticValue.FONTS_PATH.value + r"\Montserrat-Bold.ttf")
        
        self.init_window()

    def init_window(self) -> None:
        # Main layout
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.setLayout(self.main_layout)

        
        # Main frame
        self.main_frame: QWidget = QWidget()
        self.main_frame.setObjectName("main-frame")

        # main layout for main frame
        self.main_frame_layout: QHBoxLayout = QHBoxLayout()
        self.main_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.main_frame_layout.setSpacing(0)
        self.main_frame.setLayout(self.main_frame_layout)
        
        # side frame
        self.side_frame: QWidget = QWidget()
        self.side_frame.setObjectName("side-frame")
        
        # editor frame with layouts bar
        self.editor_frame: QWidget = QWidget()
        self.editor_frame.setObjectName("editor-frame")
        
        # editor frame layout
        self.editor_frame_layout: QVBoxLayout = QVBoxLayout()
        self.editor_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.editor_frame_layout.setSpacing(0)
        self.editor_frame.setLayout(self.editor_frame_layout)
        
        # layouts button frame
        self.layouts_button_frame: QWidget = QWidget()
        self.layouts_button_frame.setObjectName("layouts-button-frame")
        
        # Scroll area widget for pages
        self.scroll_area_widget: QWidget = QWidget()
        self.scroll_area_widget.setObjectName("scroll-area-widget")
        
        # scroll area layout
        self.scroll_area_layout: QVBoxLayout = QVBoxLayout()
        self.scroll_area_layout.setContentsMargins(0, 60, 0, 60)
        self.scroll_area_layout.setSpacing(40)
        self.scroll_area_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scroll_area_widget.setLayout(self.scroll_area_layout)
        
        # scroll area
        self.scroll_area: QScrollArea = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll-area")
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.editor_frame_layout.addWidget(self.layouts_button_frame)
        self.editor_frame_layout.addWidget(self.scroll_area)
        
        # a4 page frame
        self.a4_page_frame: QWidget = QWidget()
        self.a4_page_frame.setProperty("cssClass", "a4-page-frame")
        self.a4_page_frame.setObjectName("a4-page-frame")
        
        self.a4_pages_list.append(self.a4_page_frame)
        
        self.scroll_area_layout.addWidget(self.a4_page_frame)
        
        # --------------------------- Layout buttons of toolbar ---------------------------
        self.layouts_button_frame_layout: QHBoxLayout = QHBoxLayout()
        self.layouts_button_frame_layout.setContentsMargins(20, 0, 0, 0)
        self.layouts_button_frame_layout.setSpacing(35)
        self.layouts_button_frame_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.layouts_button_frame.setLayout(self.layouts_button_frame_layout)
        
        # Add buttons to the layouts button frame
        # 1x1 button
        self.icon_1x1_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "layout_1x1_icon.png")
        self.layout_1x1_button: QPushButton = QPushButton()
        self.layout_1x1_button.setProperty("cssClass", "layout-buttons")
        self.layout_1x1_button.setIcon(QIcon(self.icon_1x1_path))
        self.layout_1x1_button.setIconSize(QSize(35, 35))
        self.layout_1x1_button.setToolTip("1x1 Layout")
        self.layout_1x1_button.setObjectName("layout-1x1-button")
        
        # 2x2 button
        self.icon_2x2_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "layout_2x2_icon.png")
        self.layout_2x2_button: QPushButton = QPushButton()
        self.layout_2x2_button.setProperty("cssClass", "layout-buttons")
        self.layout_2x2_button.setIcon(QIcon(self.icon_2x2_path))
        self.layout_2x2_button.setIconSize(QSize(35, 35))   
        self.layout_2x2_button.setToolTip("2x2 Layout")
        self.layout_2x2_button.setObjectName("layout-2x2-button")
        
        # 3x2 button
        self.icon_2x3_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "layout_2x3_icon.png")
        self.layout_2x3_button: QPushButton = QPushButton()
        self.layout_2x3_button.setProperty("cssClass", "layout-buttons")
        self.layout_2x3_button.setIcon(QIcon(self.icon_2x3_path))
        self.layout_2x3_button.setIconSize(QSize(35, 35))
        self.layout_2x3_button.setToolTip("3x2 Layout")
        self.layout_2x3_button.setObjectName("layout-2x3-button")
        
        # 3x3 button
        self.icon_3x3_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "layout_3x3_icon.png")
        self.layout_3x3_button: QPushButton = QPushButton()
        self.layout_3x3_button.setProperty("cssClass", "layout-buttons")
        self.layout_3x3_button.setIcon(QIcon(self.icon_3x3_path))
        self.layout_3x3_button.setIconSize(QSize(35, 35))
        self.layout_3x3_button.setToolTip("3x3 Layout")
        self.layout_3x3_button.setObjectName("layout-3x3-button")
        
        # save file button
        self.icon_save_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "save_icon.png")
        self.save_file_button: QPushButton = QPushButton()
        self.save_file_button.setProperty("cssClass", "layout-buttons")
        self.save_file_button.setIcon(QIcon(self.icon_save_path))
        self.save_file_button.setIconSize(QSize(35, 35))
        self.save_file_button.setToolTip("Save File")
        
        # export file button
        self.icon_export_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "export_icon.png")
        self.export_file_button: QPushButton = QPushButton()
        self.export_file_button.setProperty("cssClass", "layout-buttons")
        self.export_file_button.setIcon(QIcon(self.icon_export_path))
        self.export_file_button.setIconSize(QSize(35, 35))
        self.export_file_button.setToolTip("Export File")
        
        self.radio_widget: QWidget = QWidget()
        
        self.radio_layout: QVBoxLayout = QVBoxLayout()
        self.radio_layout.setContentsMargins(0, 8, 0, 8)
        self.radio_layout.setSpacing(5)
        self.radio_widget.setLayout(self.radio_layout)
        
        # Create radio buttons
        self.radio_keep_aspect: QRadioButton = QRadioButton("Keep Aspect Ratio")
        self.radio_keep_aspect.setChecked(True)

        self.radio_resize: QRadioButton = QRadioButton("Resize")

        # Group them so only one can be selected
        self.group: QButtonGroup = QButtonGroup(self)
        self.group.addButton(self.radio_keep_aspect)
        self.group.addButton(self.radio_resize)
        
        self.group.setId(self.radio_keep_aspect, 1)
        self.group.setId(self.radio_resize, 2)

        # Connect signal to slot
        self.radio_layout.addWidget(self.radio_keep_aspect)
        self.radio_layout.addWidget(self.radio_resize)
        
        # connecting the buttons to their respective functions
        self.layout_1x1_button.clicked.connect(lambda: self.change_active_layout(self.layout_1x1_button, "1x1"))
        self.layout_2x2_button.clicked.connect(lambda: self.change_active_layout(self.layout_2x2_button, "2x2"))
        self.layout_2x3_button.clicked.connect(lambda: self.change_active_layout(self.layout_2x3_button, "2x3"))
        self.layout_3x3_button.clicked.connect(lambda: self.change_active_layout(self.layout_3x3_button, "3x3"))
        self.save_file_button.clicked.connect(self.save_file)
        self.export_file_button.clicked.connect(self.export_pdf)
        
        # add all buttons to the layouts button frame
        self.layouts_button_frame_layout.addWidget(self.layout_1x1_button)
        self.layouts_button_frame_layout.addWidget(self.layout_2x2_button)
        self.layouts_button_frame_layout.addWidget(self.layout_2x3_button)
        self.layouts_button_frame_layout.addWidget(self.layout_3x3_button)
        self.layouts_button_frame_layout.addWidget(self.save_file_button)
        self.layouts_button_frame_layout.addWidget(self.export_file_button)
        self.layouts_button_frame_layout.addWidget(self.radio_widget)
        
        # ------------------------------------------------------------------------
        # ---------------------------- Side frame buttons ----------------------------
        self.side_frame_layout: QVBoxLayout = QVBoxLayout()
        self.side_frame_layout.setContentsMargins(0, 30, 0, 0)
        self.side_frame_layout.setSpacing(20)
        self.side_frame_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.side_frame.setLayout(self.side_frame_layout)
        
        # Upload button
        self.upload_button: QPushButton = QPushButton("Upload")
        self.upload_button.setProperty("cssClass", "side-frame-buttons")
        self.upload_button.setToolTip("Upload images")
        
        # add all images button
        self.add_images_button: QPushButton = QPushButton("Add Images")
        self.add_images_button.setProperty("cssClass", "side-frame-buttons")
        self.add_images_button.setToolTip("Add uploaded images to the editor or modify the existing ones")

        # Show all button
        self.show_all_button: QPushButton = QPushButton("Show All")
        self.show_all_button.setProperty("cssClass", "side-frame-buttons")
        self.show_all_button.setEnabled(False)  # Initially disabled
        self.show_all_button.setToolTip("Show all uploaded images")
        
        # listwidget for image paths
        self.path_list_widget: QListWidget = QListWidget()
        self.path_list_widget.setObjectName("path-list-widget") 
        self.path_list_widget.setSpacing(5)
        
        self.path_list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.path_list_widget.customContextMenuRequested.connect(self.show_context_menu)
        
        self.path_list_widget.setMouseTracking(True)  # Enable mouse tracking for hover events
        self.path_list_widget.itemEntered.connect(self.show_path_on_hover)
        
        # connecting the buttons to their respective functions
        self.upload_button.clicked.connect(self.upload_images)
        self.add_images_button.clicked.connect(self.add_images_to_layout)
        self.show_all_button.clicked.connect(self.show_images)
        
        # add buttons to the side frame layout
        self.side_frame_layout.addWidget(self.upload_button)
        self.side_frame_layout.addWidget(self.add_images_button)
        self.side_frame_layout.addWidget(self.show_all_button)
        self.side_frame_layout.addWidget(self.path_list_widget)
        # ----------------------------------------------------------------------------
        
        # --------------------------------- Status bar ---------------------------------
        self.status_bar: QWidget = QWidget()
        self.status_bar.setObjectName("status-bar")
        
        self.status_bar_layout: QHBoxLayout = QHBoxLayout()
        self.status_bar_layout.setContentsMargins(0, 0, 0, 0)
        self.status_bar_layout.setSpacing(0)
        self.status_bar_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.status_bar.setLayout(self.status_bar_layout)
        
        # current layout label
        self.current_layout_label: QLabel = QLabel("Current Layout: None")
        self.current_layout_label.setObjectName("current-layout-label")       

        self.status_bar_layout.addWidget(self.current_layout_label)
        # ----------------------------------------------------------------------------
        
        self.main_frame_layout.addWidget(self.side_frame)
        self.main_frame_layout.addWidget(self.editor_frame)
        
        # self.main_layout.addWidget(self.tab_bar)        
        self.main_layout.addWidget(self.main_frame)       
        self.main_layout.addWidget(self.status_bar)       
        
        # Shortcuts
        self.upload_image_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        self.upload_image_shortcut.activated.connect(self.upload_images)

        self.add_images_shortcut: QShortcut =  QShortcut(QKeySequence("Ctrl+Alt+A"), self)
        self.add_images_shortcut.activated.connect(self.add_images_to_layout)

        self.show_all_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+Alt+S"), self)
        self.show_all_shortcut.activated.connect(self.show_images)
        self.show_all_shortcut.setEnabled(False)

        self.save_file_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.save_file_shortcut.activated.connect(self.save_file)

        self.export_file_shortcut: QShortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        self.export_file_shortcut.activated.connect(self.export_pdf)
        
        self.shortcut_1x1: QShortcut = QShortcut(QKeySequence("Alt+1"), self)
        self.shortcut_2x2: QShortcut = QShortcut(QKeySequence("Alt+2"), self)
        self.shortcut_2x3: QShortcut = QShortcut(QKeySequence("Alt+3"), self)
        self.shortcut_3x3: QShortcut = QShortcut(QKeySequence("Alt+4"), self)
        
        self.shortcut_1x1.activated.connect(lambda: self.change_active_layout(self.layout_1x1_button, "1x1"))
        self.shortcut_2x2.activated.connect(lambda: self.change_active_layout(self.layout_2x2_button, "2x2"))
        self.shortcut_2x3.activated.connect(lambda: self.change_active_layout(self.layout_2x3_button, "2x3"))
        self.shortcut_3x3.activated.connect(lambda: self.change_active_layout(self.layout_3x3_button, "3x3"))
        
        self.keep_ratio_shortcut: QShortcut = QShortcut(QKeySequence("Alt+K"), self)
        self.keep_ratio_shortcut.activated.connect(lambda: self.radio_keep_aspect.setChecked(True))

        self.resize_shortcut: QShortcut = QShortcut(QKeySequence("Alt+R"), self)
        self.resize_shortcut.activated.connect(lambda: self.radio_resize.setChecked(True))
        
        self.delete_item_shortcut: QShortcut = QShortcut(QKeySequence("Delete"), self.path_list_widget)
        self.delete_item_shortcut.activated.connect(self.remove_item)
    
    def change_active_layout(self, sender: QObject , layout: str) -> None:

        if self.active_layout == "1x1" and sender.objectName() == "layout-1x1-button":
            self.layout_1x1_button.setIcon(QIcon(self.icon_1x1_path))
            self.active_layout = None
        elif self.active_layout == "2x2" and sender.objectName() == "layout-2x2-button":
            self.layout_2x2_button.setIcon(QIcon(self.icon_2x2_path))
            self.active_layout = None
        elif self.active_layout == "2x3" and sender.objectName() == "layout-2x3-button":
            self.layout_2x3_button.setIcon(QIcon(self.icon_2x3_path))
            self.active_layout = None
        elif self.active_layout == "3x3" and sender.objectName() == "layout-3x3-button":
            self.layout_3x3_button.setIcon(QIcon(self.icon_3x3_path))
            self.active_layout = None
            
        elif layout == "1x1":
            self.active_layout = "1x1"
            
            self.layout_2x2_button.setIcon(QIcon(self.icon_2x2_path))
            self.layout_2x3_button.setIcon(QIcon(self.icon_2x3_path))
            self.layout_3x3_button.setIcon(QIcon(self.icon_3x3_path))
            
            self.active_1x1_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "active_1x1_icon.png")
            self.layout_1x1_button.setIcon(QIcon(self.active_1x1_path)) 
        elif layout == "2x2":
            self.active_layout = "2x2"

            self.layout_1x1_button.setIcon(QIcon(self.icon_1x1_path))
            self.layout_2x3_button.setIcon(QIcon(self.icon_2x3_path))
            self.layout_3x3_button.setIcon(QIcon(self.icon_3x3_path))

            self.active_2x2_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "active_2x2_icon.png")
            self.layout_2x2_button.setIcon(QIcon(self.active_2x2_path)) 
        elif layout == "2x3":
            self.active_layout = "2x3"

            self.layout_1x1_button.setIcon(QIcon(self.icon_1x1_path))
            self.layout_2x2_button.setIcon(QIcon(self.icon_2x2_path))
            self.layout_3x3_button.setIcon(QIcon(self.icon_3x3_path))

            self.active_2x3_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "active_2x3_icon.png")
            self.layout_2x3_button.setIcon(QIcon(self.active_2x3_path)) 
        elif layout == "3x3":
            self.active_layout = "3x3"

            self.layout_1x1_button.setIcon(QIcon(self.icon_1x1_path))
            self.layout_2x2_button.setIcon(QIcon(self.icon_2x2_path))
            self.layout_2x3_button.setIcon(QIcon(self.icon_2x3_path))

            self.active_3x3_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value, "active_3x3_icon.png")
            self.layout_3x3_button.setIcon(QIcon(self.active_3x3_path)) 
            
        self.current_layout_label.setText(f"Current Layout: {self.active_layout}")
        
    def show_path_on_hover(self, item) -> None:
        self.path_list_widget.setToolTip(item.text()) 
        
    def upload_images(self) -> None:
        # Open file dialog to select images
        file_dialog: QFileDialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_dialog.setViewMode(QFileDialog.ViewMode.List)
        
        # getting the image paths
        if file_dialog.exec():
            selected_files: list[str] = file_dialog.selectedFiles()
            self.images_paths_list.extend(selected_files)
            self.show_all_button.setEnabled(True)
            self.show_all_shortcut.setEnabled(True)
            
            for file_path in selected_files:
                item: QListWidgetItem = QListWidgetItem(file_path)
                self.path_list_widget.addItem(item)
                
    def set_layout(self) -> list[int]:
        img_dimensions: list[int] = []
        
        if self.active_layout == "1x1":
            # Set the layout to 1x1
            img_width: int = (self.page_width) - 50
            img_height: int = (self.page_height) - 50
            img_dimensions = [img_width, img_height]
        
        if self.active_layout == "2x2":
            # Set the layout to 2x2
            img_width: int = (self.page_width // 2) - 50
            img_height: int = (self.page_height // 2) - 50
            img_dimensions = [img_width, img_height]
            
        if self.active_layout == "2x3":
            # Set the layout to 2x3
            img_width: int = (self.page_width // 2) - 50
            img_height: int = (self.page_height // 3) - 50
            img_dimensions = [img_width, img_height]
            
        if self.active_layout == "3x3":
            # Set the layout to 3x3
            img_width: int = (self.page_width // 3) - 50
            img_height: int = (self.page_height // 3) - 50
            img_dimensions = [img_width, img_height]
            
        return img_dimensions
    
    def add_images_to_layout(self) -> None:            
        if not self.images_paths_list:
            self.noimages_dialog: NoImagesDialog = NoImagesDialog()
            self.noimages_dialog.show()

            return
        
        if self.active_layout == None:
            self.nolayout_dialog: NoLayoutDialog = NoLayoutDialog()
            self.nolayout_dialog.show()
            
            return
        
        radio_id: int = self.group.checkedId()
        
        img_dimensions: list[int] = self.set_layout()
        
        self.a4_page_frame_layout: QGridLayout = QGridLayout()
        self.a4_page_frame_layout.setContentsMargins(30, 20, 20, 20)
        self.a4_page_frame_layout.setSpacing(10)
        
        self.a4_pages_layout_list.append(self.a4_page_frame_layout)
        
        self.a4_page_frame.setLayout(self.a4_page_frame_layout)
        
        for child in self.a4_page_frame.findChildren(QWidget):
            child.setParent(None)
            child.deleteLater()
        
        for i in range(1, len(self.a4_pages_list)):
            self.scroll_area_layout.removeWidget(self.a4_pages_list[i])
            self.a4_pages_list[i].setParent(None)
            self.a4_pages_list[i].deleteLater()
            
        self.a4_pages_list = [self.a4_pages_list[0]]
        self.a4_pages_layout_list = [self.a4_pages_layout_list[0]]
                
        calc_layout: str = self.active_layout.replace("x", "*")
        calc: int = eval(calc_layout)
        pages_required: int = len(self.images_paths_list) // calc
        
        self.editFile.emit(self, self.current_file, "edited")
        self.add_images(pages_required=pages_required, radio_id=radio_id, img_dimensions=img_dimensions)
        
    def add_images(self, pages_required: int, radio_id: int, img_dimensions: list[int]) -> None:
        if pages_required > 0:
            for l in range(pages_required):
                a4_page_frame: QWidget = QWidget()
                a4_page_frame.setProperty("cssClass", "a4-page-frame")
                # a4_page_frame.setObjectName("a4-page-frame")
                
                self.a4_pages_list.append(a4_page_frame)
                
                a4_page_frame_layout: QGridLayout = QGridLayout()
                a4_page_frame_layout.setContentsMargins(30, 20, 20, 20)
                a4_page_frame_layout.setSpacing(10)
                
                self.a4_pages_layout_list.append(a4_page_frame_layout)
                
                a4_page_frame.setLayout(a4_page_frame_layout)
                
                self.scroll_area_layout.addWidget(a4_page_frame)    
        
        if self.active_layout == "1x1":            
            for i in range(len(self.images_paths_list)):                
                try:
                    path: str = self.images_paths_list[i]
                except IndexError:
                    break
                
                current_a4_page_layout: QGridLayout = self.a4_pages_layout_list[i]
                
                target_size: QSize = QSize(img_dimensions[0], img_dimensions[1])
                
                if radio_id == 1:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                elif radio_id == 2:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size)

                label: QLabel = QLabel()
                label.setPixmap(pixmap)

                current_a4_page_layout.addWidget(label, 0, 0)
        
        elif self.active_layout == "2x2":
            j = 0
            index = 0
            current_a4_page_layout: QGridLayout = self.a4_pages_layout_list[index]
            
            for i in range(len(self.images_paths_list)):                
                try:
                    path: str = self.images_paths_list[i]
                except IndexError:
                    break
                
                if i % 4 == 0 and i != 0:
                    j = 0
                    index += 1
                    current_a4_page_layout = self.a4_pages_layout_list[index]
                
                target_size: QSize = QSize(img_dimensions[0], img_dimensions[1])
                
                if radio_id == 1:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                elif radio_id == 2:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size)
                    
                label: QLabel = QLabel()
                label.setPixmap(pixmap)
                
                row: int = j // 2
                col: int = j % 2
                current_a4_page_layout.addWidget(label, row, col)
                
                j += 1
                
        elif self.active_layout == "2x3":
            j = 0
            index = 0
            print(index)
            current_a4_page_layout: QGridLayout = self.a4_pages_layout_list[index]
            
            for i in range(len(self.images_paths_list)):
                try:
                    path: str = self.images_paths_list[i]
                except IndexError:
                    break
                
                if i % 6== 0 and i != 0:
                    j = 0
                    index += 1
                    current_a4_page_layout = self.a4_pages_layout_list[index]
                
                target_size: QSize = QSize(img_dimensions[0], img_dimensions[1])
                
                if radio_id == 1:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                elif radio_id == 2:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size)
                    
                label: QLabel = QLabel()
                label.setPixmap(pixmap)
                
                row: int = j// 2
                col: int = j % 2
                current_a4_page_layout.addWidget(label, row, col)
                
                j += 1
                
        elif self.active_layout == "3x3":
            j = 0
            index = 0
            current_a4_page_layout: QGridLayout = self.a4_pages_layout_list[index]
            
            for i in range(len(self.images_paths_list)):
                try:
                    path: str = self.images_paths_list[i]
                except IndexError:
                    break
                
                if i % 9 == 0 and i != 0:
                    j = 0
                    index += 1
                    current_a4_page_layout = self.a4_pages_layout_list[index]
                
                target_size: QSize = QSize(img_dimensions[0], img_dimensions[1])
                
                if radio_id == 1:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                elif radio_id == 2:
                    pixmap: QPixmap = QPixmap(path).scaled(target_size)
                    
                label: QLabel = QLabel()
                label.setPixmap(pixmap)
                
                row: int = j // 3
                col: int = j % 3
                
                current_a4_page_layout.addWidget(label, row, col)
                
                j += 1
                
    def show_images(self) -> None:
            self.images_window: ImagesWindow = ImagesWindow(self.images_paths_list)
            self.images_window.show()
            
    def show_context_menu(self, pos: QPoint) -> None:
        item: QListWidgetItem = self.path_list_widget.itemAt(pos)
        
        if item is None:
            return
        
        menu = QMenu()
        with open(f"{EditorStaticValue.CSS_PATH.value + r'\editor.qss'}", "r") as file_:
            menu.setStyleSheet(file_.read())

        icon_path: str = os.path.join(EditorStaticValue.ICONS_PATH.value + r"\delete_icon.png")
        action_delete: QAction = menu.addAction(QIcon(icon_path), "Delete")

        action: QAction = menu.exec(self.path_list_widget.mapToGlobal(pos))
        
        if action == action_delete:
            self.delete_item(item=item)
            
    def delete_item(self, item: QListWidgetItem) -> None:
        index: int = self.path_list_widget.row(item)
        self.path_list_widget.takeItem(index)
        self.images_paths_list.pop(index)
        
        if len(self.images_paths_list) == 0:
            self.show_all_button.setEnabled(False)
            self.show_all_shortcut.setEnabled(False)
        
    def export_pdf(self) -> None:
        dialog: QFileDialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["PDF Files (*.pdf)", "All Files (*)"])
        dialog.selectNameFilter("PDF Files (*.pdf)")
        dialog.setWindowTitle("Save PDF As")

        if dialog.exec():
            selected_file = dialog.selectedFiles()[0]
            self.export_widgets_to_pdf(self.a4_pages_list, selected_file)
        
    def export_widgets_to_pdf(self, widgets: list[QWidget], output_file: str):

        printer: QPrinter = QPrinter(QPrinter.PrinterMode.HighResolution)
        printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
        printer.setPageSize(QPageSize(QPageSize.PageSizeId.A4))
        printer.setFullPage(True)
        printer.setOutputFileName(output_file)

        painter: QPainter = QPainter()
        if not painter.begin(printer):
            QMessageBox.critical(self, "Error", "Failed to start PDF export.")
            return

        progress_dialog = QProgressDialog("Exporting PDF...", "Cancel", 0, len(widgets), self)
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setCancelButton(None)
        progress_dialog.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        progress_dialog.show()

        state = {"index": 0}

        self.progressdone_dialog: ProgressDoneDialog = ProgressDoneDialog()                    

        def render_next():
            i = state["index"]
            if progress_dialog.wasCanceled() or i >= len(widgets):
                painter.end()
                progress_dialog.close()
                if i >= len(widgets):
                    self.progressdone_dialog.show()
                return

            widget = widgets[i]
            if i > 0:
                printer.newPage()

            page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
            scale = min(page_rect.width() / widget.width(), page_rect.height() / widget.height())
            x_offset = (page_rect.width() - widget.width() * scale) / 2
            y_offset = (page_rect.height() - widget.height() * scale) / 2

            painter.save()
            painter.translate(x_offset, y_offset)
            painter.scale(scale, scale)
            widget.render(painter, QPoint(0, 0))
            painter.restore()

            state["index"] += 1
            progress_dialog.setValue(state["index"])
            QApplication.processEvents()
            QTimer.singleShot(0, render_next)  # Queue next step

        QTimer.singleShot(0, render_next)
       
    def generate_json_data(self) -> str:
        layout: str = self.active_layout
        pages: int = len(self.a4_pages_list)
        images: list[str] = self.images_paths_list
        aspect: str = "keep" if (self.group.checkedId() == 1) else "resize"
        
        json_data: dict = {
                            "pages": pages,
                            "layout": layout,
                            "images": images,
                            "aspect-ratio": aspect
        }
        
        return json_data

    def save_file(self) -> None:
        if self.current_file != None:
            data: str = self.generate_json_data()
            json_data: str = json.dumps(data)
            encoded_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")

            with open(self.current_file, "w") as file_:
                file_.write(encoded_data)
                
            self.saveFile.emit(self, self.current_file, "saved")
            self.saveSignal.emit(self.current_file, "exist")

            return
        
        dialog: QFileDialog = QFileDialog(self)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(["Imject Files (*.imject)", "All Files (*)"])
        dialog.selectNameFilter("Imject Files (*.imject)")
        dialog.setWindowTitle("Save File As")
        
        if not dialog.exec():
            return
        
        file_path: str = dialog.selectedFiles()[0]
        self.current_file = file_path

        data: str = self.generate_json_data()
        json_data: str = json.dumps(data)
        encoded_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")

        with open(self.current_file, "w") as file_:
            file_.write(encoded_data)
            
        self.saveFile.emit(self, self.current_file, "saved")
        self.saveSignal.emit(self.current_file, "new")
            
    def open_file_(self, json_data: str) -> None:
        layout: str = json_data["layout"]           
        pages: int = (json_data["pages"]-1)
        self.images_paths_list.clear()

        self.a4_page_frame_layout: QGridLayout = QGridLayout()
        self.a4_page_frame_layout.setContentsMargins(30, 20, 20, 20)
        self.a4_page_frame_layout.setSpacing(10)
        self.a4_page_frame.setLayout(self.a4_page_frame_layout)
        
        self.a4_pages_layout_list.append(self.a4_page_frame_layout)  
        
        self.images_paths_list.extend(json_data["images"])
        
        if len(self.images_paths_list) > 0:
            self.show_all_button.setEnabled(True)
        
        for img_path in self.images_paths_list:
            item: QListWidgetItem = QListWidgetItem(img_path)
            self.path_list_widget.addItem(item)

        radio_id: int = 1 if (json_data["aspect-ratio"] == "keep") else 2
        
        self.current_layout_label.setText(f"Current Layout: {self.active_layout}")
        
        if layout == "1x1":
            self.change_active_layout(self.layout_1x1_button, "1x1")
        elif layout == "2x2":
            self.change_active_layout(self.layout_2x2_button, "2x2")
        elif layout == "2x3":
            self.change_active_layout(self.layout_2x3_button, "2x3")
        elif layout == "3x3":
            self.change_active_layout(self.layout_3x3_button, "3x3")
    
        img_dimensions: list[int] = self.set_layout()
        self.add_images(pages_required=pages, radio_id=radio_id, img_dimensions=img_dimensions)

    def change_file_path(self, path_:str) -> None:
        self.current_file = path_
        
    def remove_item(self) -> None:
        for item in self.path_list_widget.selectedItems():
            index: int = self.path_list_widget.row(item)
            self.path_list_widget.takeItem(index)
            self.images_paths_list.pop(index)
            
        if len(self.images_paths_list) == 0:
            self.show_all_button.setEnabled(False)
            self.show_all_shortcut.setEnabled(False)
        
if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    app.setStyle("Fusion")
    window: EditorWindow = EditorWindow()
    window.show()
    sys.exit(app.exec())