import numpy as np
import vispy.scene
from PySide6.QtWidgets import QWidget, QVBoxLayout
from vispy.color import ColorArray
from vispy.scene import visuals


class PointCloudCanvas:

    def __init__(self, points, centroid):
        self.point_cloud = points

        self.canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        view = self.canvas.central_widget.add_view()

        pos = self.point_cloud[['x', 'y', 'z']].values

        colors_columns = ['red', 'green', 'blue']
        if 'opacity' in self.point_cloud:
            colors_columns.append('opacity')

        colarr = ColorArray(color=self.point_cloud[colors_columns].values, clip=True)

        # create scatter object and fill in the data
        scatter = visuals.Markers()
        scatter.set_data(pos, edge_width=0, face_color=colarr, size=3)

        view.add(scatter)

        view.camera = 'turntable'  # or try 'arcball'
        view.camera.center = centroid

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=view.scene)


class PointCloudWidget(QWidget):

    def __init__(self, point_cloud):
        super().__init__()

        main_layout = QVBoxLayout()

        self.canvas = PointCloudCanvas(point_cloud.points, point_cloud.centroid)
        self.canvas.canvas.show()

        main_layout.addWidget(self.canvas.canvas.native)
        self.setLayout(main_layout)


def prepare_point_cloud(point_cloud, flip=False, normalize_colors=False):
    perc = np.percentile(point_cloud.points[['red', 'green', 'blue']], 99, 0)

    if any(perc) > 1.0:

        print("Normalize colors")

        point_cloud.points['red'] = point_cloud.points['red'] / 255.0
        point_cloud.points['green'] = point_cloud.points['green'] / 255.0
        point_cloud.points['blue'] = point_cloud.points['blue'] / 255.0

    if flip:
        point_cloud.points['z'] = point_cloud.points['z'] * -1

    if 'a' in point_cloud.points or  'scalar_a' in point_cloud.points:
        key = 'a' if 'a' in point_cloud.points else 'scalar_a'
        point_cloud.points['opacity'] = 1 / (1 + np.exp(-point_cloud.points[key]))

    if 'scale_x' in point_cloud.points:
        point_cloud.points['scale_x'] = np.exp(point_cloud.points['s0'])
        point_cloud.points['scale_y'] = np.exp(point_cloud.points['s1'])
        point_cloud.points['scale_z'] = np.exp(point_cloud.points['s2'])

    point_cloud.points.astype(np.float32)
