from PySide6.QtCore import QObject, QUrl, Qt 
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMainWindow, QHBoxLayout, QStackedLayout, QFileDialog, QGridLayout, QLabel
from pyntcloud import PyntCloud
from src.rendering.render_point_cloud import prepare_point_cloud

from ..config import HEADER_FILE, FOOTER_FILE, LEFT_PANE_FILE, RIGHT_PANE_LB_FILE, RIGHT_PANE_LT_FILE, RIGHT_PANE_RB_FILE, RIGHT_PANE_RT_FILE

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

    def _create_right_pane_lt(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_LT_FILE, parent)
    
    def _create_right_pane_lb(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_LB_FILE, parent)

    def _create_right_pane_rt(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_RT_FILE, parent)

    def _create_right_pane_rb(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_RB_FILE, parent)

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

        lt = self._create_right_pane_lt(self._renderer_cont)
        rt = self._create_right_pane_rt(self._renderer_cont)
        lb = self._create_right_pane_lb(self._renderer_cont)
        rb = self._create_right_pane_rb(self._renderer_cont)
        lt.setFixedSize(200, 70)
        rt.setFixedSize(70, 140)
        lb.setFixedSize(200, 140)
        rb.setFixedSize(210, 70)
        self._renderer_layout.addWidget(lt, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self._renderer_layout.addWidget(rt, 0, 1, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self._renderer_layout.addWidget(lb, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self._renderer_layout.addWidget(rb, 1, 1, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)