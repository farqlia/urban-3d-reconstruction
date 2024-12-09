import sys
import time

from PySide6.QtWidgets import QApplication
from src.pipeline.model_processor import ModelProcessor
from src.frontend.view import View
from src.backend.controller import Controller
from src.rendering.rendering_library import RenderingLibrary

if __name__ == '__main__':
    lib = RenderingLibrary()

    app = QApplication(sys.argv)
    mp = ModelProcessor()
    controller = Controller(mp)
    view = View(controller, lib.lib)

    view.run()
    sys.exit(app.exec())

    lib.cleanUp()
    lib.close()