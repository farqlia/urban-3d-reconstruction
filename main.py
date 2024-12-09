import sys
import time

from PySide6.QtWidgets import QApplication
from src.frontend.view import View
from src.backend.controller import Controller
from src.urb3d.pipeline.backend import Backend
from src.urb3d.rendering.rendering_library import RenderingLibrary

if __name__ == '__main__':
    lib = RenderingLibrary()

    app = QApplication(sys.argv)
    backend = Backend()
    controller = Controller(backend)
    view = View(controller, lib.lib)

    view.run()
    sys.exit(app.exec())

    lib.cleanUp()
    lib.close()