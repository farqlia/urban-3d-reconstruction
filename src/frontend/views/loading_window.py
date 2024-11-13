from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QMovie
from PySide6.QtQuickWidgets import QQuickWidget

from ..config import LOADING_WINDOW_FILE

class LoadingWindow(QQuickWidget):
    def __init__(self, engine_manager, parent):
        super().__init__(engine_manager, parent)
        self.setSource(QUrl.fromLocalFile(LOADING_WINDOW_FILE))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        

# class LoadingWindow(QWidget):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
#         self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#         self.setStyleSheet(
#             """QWidget {
#                 border: 5px solid #ABB2BF;
#                 border-radius: 10px;
#             }"""
#         )
#         parent_rect = parent.rect()
#         self.setGeometry(
#             (parent_rect.width() - 200) // 2,
#             (parent_rect.height() - 200) // 2,
#             200,
#             200
#         )

#         layout = QVBoxLayout(self)

#         spinner = QLabel(self)
#         spinner.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         animation = QMovie("src/frontend/views/icons/loading.gif")
#         spinner.setMovie(animation)
#         animation.start()

#         message = QLabel("Loading", self)
#         message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
#         layout.addWidget(spinner)
#         layout.addWidget(message)

