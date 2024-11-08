import sys
from PySide6.QtWidgets import QApplication
from pathlib import Path
from pyntcloud import PyntCloud

from src.rendering.render_point_cloud import MainWindow, prepare_point_cloud

if __name__ == "__main__":

    point_cloud_file = "../data/c7_sparse.ply"
    point_cloud = PyntCloud.from_file(point_cloud_file)
    prepare_point_cloud(point_cloud)

    app = QApplication(sys.argv)

    window = MainWindow(point_cloud.points)
    window.show()
    sys.exit(app.exec())
