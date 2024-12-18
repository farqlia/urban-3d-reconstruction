from PySide6.QtCore import QObject, QUrl, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QHBoxLayout, QStackedLayout, QFileDialog, QGridLayout, QLabel, QApplication, QSizePolicy
from PySide6.QtGui import QPixmap
import os

from ..config import HEADER_FILE, FOOTER_FILE, LEFT_PANE_FILE, RIGHT_PANE_LB_FILE, RIGHT_PANE_LT_FILE, RIGHT_PANE_RB_FILE, RIGHT_PANE_RT_FILE
from .sliding_widget import SlidingWidget

class MainWindow(QMainWindow):
    def __init__(self, parent, engine_manager, lib):
        super(MainWindow, self).__init__()

        self.parent = parent

        self.setWindowTitle("Urb3D - Urban 3D reconstruction and segmentation")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen_geometry.width(), screen_geometry.height())

        self.body = None

        self.showMaximized()

        self._engine_manager = engine_manager

        central_widget = QWidget()
        central_widget.setGeometry(0, 0, self.width(), self.height())
        central_layout = QVBoxLayout(central_widget)
        
        central_widget.setStyleSheet(
            "background-color: #282C34"
        )

        header = self._create_header(central_widget)
        footer = self._create_footer(central_widget)
        self.body = SlidingWidget(central_widget, self._engine_manager)

        header.setMinimumHeight(100)
        header.setMaximumHeight(120)
        footer.setMaximumHeight(20)

        self.setCentralWidget(central_widget)

        central_layout.addWidget(header)
        central_layout.addWidget(self.body)
        central_layout.addWidget(footer)

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

    def configure_renderer(self, renderer, viz_type):
        self.body.update_right_pane(renderer, viz_type)
    
    def slide_body(self):
        self.body.toggle_widgets()

    def resizeEvent(self, event):
        if self.body is not None:
            self.body.update_geometry(self.geometry())
        super().resizeEvent(event)

    def closeEvent(self, event):
        print("CLOSING")
        # No cleaning up lib
        event.accept()
