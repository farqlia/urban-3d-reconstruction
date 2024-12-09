from PySide6.QtCore import QPropertyAnimation, QRect, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QWidget, QGridLayout
from ..config import HEADER_FILE, FOOTER_FILE, LEFT_PANE_FILE, RIGHT_PANE_LB_FILE, RIGHT_PANE_LT_FILE, RIGHT_PANE_RB_FILE, RIGHT_PANE_RT_FILE
from ..view_engine_manager import EngineManager

class SlidingWidget(QWidget):
    def __init__(self, parent, engine_manager):
        super().__init__(parent)

        self.setGeometry(0, 0, parent.geometry().width() - 20, parent.geometry().height() - 320) #TODO Fix - should be auto in final

        self._engine_manager = engine_manager
        self.renderer = None

        # self.toggle_button = QPushButton("Show Widget", self)
        # self.toggle_button.setGeometry(350, 500, 100, 40)
        # self.toggle_button.clicked.connect(self.toggle_widgets)

        parent_position = self.geometry()

        self.left_widget_visible = True

        self.left_widget = self.create_left_widget(self)
        self.left_widget.setGeometry(parent_position.x(), parent_position.y(), 300, parent_position.height())
        left_position = self.left_widget.geometry()
        self.right_widget = QWidget(self)
        # self.right_widget.setStyleSheet("background-color: red;")
        self.right_widget.setGeometry(parent_position.x() + 320, parent_position.y(), parent_position.width() - 320, parent_position.height())
        self.right_layout = QGridLayout(self.right_widget)
        self.update_right_pane(self.renderer)

        self.left_animation = QPropertyAnimation(self.left_widget, b"geometry", self)
        self.right_animation = QPropertyAnimation(self.right_widget, b"geometry", self)

    def create_left_widget(self, parent):
        return self._engine_manager.load_component(LEFT_PANE_FILE, parent)

    def create_right_pane_lt(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_LT_FILE, parent)
    
    def create_right_pane_lb(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_LB_FILE, parent)

    def create_right_pane_rt(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_RT_FILE, parent)

    def create_right_pane_rb(self, parent):
        return self._engine_manager.load_component(RIGHT_PANE_RB_FILE, parent)

    def update_right_pane(self, renderer):
        if self.renderer is not None:
            self.renderer.hide()
            self.renderer = None
        
        self.renderer = renderer

        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

        if self.renderer is not None:
            self.right_layout.addWidget(self.renderer, 0, 0, 2, 2)

        lt = self.create_right_pane_lt(self.right_widget)
        rt = self.create_right_pane_rt(self.right_widget)
        lb = self.create_right_pane_lb(self.right_widget)
        rb = self.create_right_pane_rb(self.right_widget)
        lt.setFixedSize(200, 70)
        rt.setFixedSize(70, 140)
        lb.setFixedSize(200, 140)
        rb.setFixedSize(210, 70)
        self.right_layout.addWidget(lt, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.right_layout.addWidget(rt, 0, 1, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.right_layout.addWidget(lb, 1, 0, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
        self.right_layout.addWidget(rb, 1, 1, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        self.right_layout.setRowStretch(0, 1)
        self.right_layout.setRowStretch(1, 1)
        self.right_layout.setColumnStretch(0, 1)
        self.right_layout.setColumnStretch(1, 1)
    
    def toggle_widgets(self):
        self.left_animation.stop()
        self.right_animation.stop()

        left = self.left_widget.geometry()
        right = self.right_widget.geometry()

        if self.left_widget_visible:
            self.left_animation.setStartValue(left)
            self.left_animation.setEndValue(QRect(-left.width(), left.y(), left.width(), left.height()))

            self.right_animation.setStartValue(right)
            self.right_animation.setEndValue(QRect(right.x()-left.width()-20, right.y(), right.width()+left.width(), right.height()))
        else:
            self.left_animation.setStartValue(left)
            self.left_animation.setEndValue(QRect(0, left.y(), left.width(), left.height()))

            self.right_animation.setStartValue(right)
            self.right_animation.setEndValue(QRect(right.x()+left.width()+20, right.y(), right.width()-left.width(), right.height()))
        
        self.left_animation.setDuration(500)
        self.right_animation.setDuration(500)

        self.left_animation.start()
        self.right_animation.start()

        self.left_widget_visible = not self.left_widget_visible
