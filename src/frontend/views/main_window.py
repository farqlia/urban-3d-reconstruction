from PySide6.QtCore import QObject, QUrl, Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QHBoxLayout, QStackedLayout, QFileDialog, QGridLayout, QLabel, QApplication, QSizePolicy

from ..config import HEADER_FILE, FOOTER_FILE, LEFT_PANE_FILE, RIGHT_PANE_LB_FILE, RIGHT_PANE_LT_FILE, RIGHT_PANE_RB_FILE, RIGHT_PANE_RT_FILE
from .sliding_widget import SlidingWidget

class MainWindow(QMainWindow):
    def __init__(self, engine_manager):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Urb3D - Urban 3D reconstruction and segmentation")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        self.showMaximized()

        self._engine_manager = engine_manager
        self._renderer = None

        central_widget = QWidget()
        central_widget.setGeometry(0, 0, self.width(), self.height())
        central_layout = QVBoxLayout(central_widget)
        
        central_widget.setStyleSheet(
            "background-color: #282C34"
        )

        header = self._create_header(central_widget)
        footer = self._create_footer(central_widget)
        self.body = SlidingWidget(central_widget, self._engine_manager)
        # body = QWidget(central_widget)
        # body.setWindowModality(Qt.WindowModality.ApplicationModal)
        # body_layout = QHBoxLayout(body)

        header.setMinimumHeight(100)
        header.setMaximumHeight(100)
        footer.setMaximumHeight(20)

        # lp_cont = QWidget(body)
        # lp_cont_layout = QVBoxLayout(lp_cont)
        # lp_cont.setMaximumWidth(300)
        # left_pane = self._create_left_pane(lp_cont)
        # lp_cont_layout.addWidget(left_pane)

        # self._renderer_cont = QWidget(body)
        # self._renderer_layout = QGridLayout(self._renderer_cont)

        # self._update_right_pane()

        # body.setMaximumHeight(700)

        # body_layout.addWidget(lp_cont, stretch=1)
        # body_layout.addWidget(self._renderer_cont, stretch=4)

        central_layout.addWidget(header)
        central_layout.addWidget(self.body)
        central_layout.addWidget(footer)

        self.setCentralWidget(central_widget)
    
    def _create_header(self, parent):
        return self._engine_manager.load_component(HEADER_FILE, parent)
    
    def _create_footer(self, parent):
        return self._engine_manager.load_component(FOOTER_FILE, parent)
    
    def _create_left_pane(self, parent):
        return self._engine_manager.load_component(LEFT_PANE_FILE, parent)

    def _create_right_pane_lt(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_LT_FILE, parent)
    
    def _create_right_pane_lb(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_LB_FILE, parent)

    def _create_right_pane_rt(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_RT_FILE, parent)

    def _create_right_pane_rb(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_RB_FILE, parent)

    def configure_renderer(self, renderer):
        # self._renderer.setParent()
        # self._renderer.hide()
        self.body.update_right_pane(renderer)
        # self._renderer.show()
    
    def slide_body(self):
        self.body.toggle_widgets()
