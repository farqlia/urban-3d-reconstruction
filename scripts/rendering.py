import sys
from PySide6.QtWidgets import QApplication

from src.rendering.render_point_cloud import MainWindow, generate_random_point_cloud

if __name__ == "__main__":
    app = QApplication(sys.argv)
    point_cloud = generate_random_point_cloud()

    window = MainWindow(point_cloud)
    window.show()
    sys.exit(app.exec())
