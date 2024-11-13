from PySide6.QtCore import QObject, QUrl, Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QHBoxLayout, QStackedLayout, QFileDialog, QGridLayout, QLabel
from pyntcloud import PyntCloud
from src.rendering.render_point_cloud import PointCloudGLWidget, prepare_point_cloud

from ..config import HEADER_FILE, FOOTER_FILE, LEFT_PANE_FILE

class MainWindow(QMainWindow):
    def __init__(self, engine_manager):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Urb3D - Urban 3D reconstruction and segmentation")
        self.setGeometry(100, 100, 1600, 900)
        self.setFixedSize(1600, 900)

        self._engine_manager = engine_manager
        self._renderer = None

        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        
        central_widget.setStyleSheet(
            "background-color: #282C34"
        )

        header = self._create_header(central_widget)
        footer = self._create_footer(central_widget)
        body = QWidget(central_widget)
        # body.setWindowModality(Qt.WindowModality.ApplicationModal)
        body_layout = QHBoxLayout(body)

        header.setMaximumHeight(100)
        footer.setMaximumHeight(20)

        lp_cont = QWidget(body)
        lp_cont_layout = QVBoxLayout(lp_cont)
        lp_cont.setMaximumWidth(300)
        left_pane = self._create_left_pane(lp_cont)
        lp_cont_layout.addWidget(left_pane)

        self._renderer_cont = QWidget(body)
        self._renderer_layout = QGridLayout(self._renderer_cont)

        self._update_right_pane()

        body.setMaximumHeight(700)

        body_layout.addWidget(lp_cont)
        body_layout.addWidget(self._renderer_cont)

        central_layout.addWidget(header)
        central_layout.addWidget(body)
        central_layout.addWidget(footer)

        self.setCentralWidget(central_widget)
    
    def _create_header(self, parent):
        return self._engine_manager.load_component(HEADER_FILE, parent)
    
    def _create_footer(self, parent):
        return self._engine_manager.load_component(FOOTER_FILE, parent)
    
    def _create_left_pane(self, parent):
        return self._engine_manager.load_component(LEFT_PANE_FILE, parent)
    
    def configure_renderer(self, renderer):
        # For now
        if self._renderer is not None:
            self._renderer.hide()
            self._renderer = None
        self._renderer = renderer
        # self._renderer.setParent()
        # self._renderer.hide()
        self._update_right_pane()
        # self._renderer.show()

    def _update_right_pane(self):
        while self._renderer_layout.count():
            item = self._renderer_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        if self._renderer is not None:
            self._renderer_layout.addWidget(self._renderer, 0, 0, 2, 2)
        
        for row in range(2):
            for col in range(2):
                cell_widget = QLabel(f"r: {row}, c: {col}", self._renderer_cont)
                cell_widget.setStyleSheet("background: transparent")
                self._renderer_layout.addWidget(cell_widget, row, col)
        