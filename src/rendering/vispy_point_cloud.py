import sys

import numpy as np
import vispy.scene
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication
from vispy.scene import visuals
from vispy.color import ColorArray
from pyntcloud import PyntCloud
from vispy import app

# conda install -c conda-forge pyqt

class PointCloudCanvas:

    def __init__(self, points):
        self.point_cloud = points

        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        view = self.canvas.central_widget.add_view()

        pos = self.point_cloud[['x', 'y', 'z']].values
        colarr = ColorArray(color=self.point_cloud[['red', 'green', 'blue', 'opacity']].values, clip=True)

        # create scatter object and fill in the data
        scatter = visuals.Markers()
        scatter.set_data(pos, edge_width=0, face_color=colarr, size=3)

        view.add(scatter)

        view.camera = 'turntable'  # or try 'arcball'

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=view.scene)


class PointCloudWidget(QWidget):

    def __init__(self, point_cloud):
        super().__init__()

        main_layout = QVBoxLayout()

        self.canvas = PointCloudCanvas(point_cloud)
        self.canvas.canvas.show()

        main_layout.addWidget(self.canvas.canvas.native)
        self.setLayout(main_layout)