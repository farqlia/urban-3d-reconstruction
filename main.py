import sys
import time

from PySide6.QtWidgets import QApplication
from src.frontend.view import View
from src.backend.controller import Controller
from src.urb3d.pipeline.backend import Backend

if __name__ == '__main__':
    app = QApplication(sys.argv)
    backend = Backend()
    controller = Controller(backend)
    view = View(controller, None) # version without lib

    view.run()
    sys.exit(app.exec())