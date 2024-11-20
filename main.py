import sys

from PySide6.QtWidgets import QApplication
from src.pipeline.model_processor import ModelProcessor
from src.frontend.view import View
from src.backend.controller import Controller

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mp = ModelProcessor()
    controller = Controller(mp)
    view = View(controller)

    view.run()
    sys.exit(app.exec())