import numpy as np
import pandas as pd
import vispy.scene
from vispy.scene import visuals
from vispy.color import ColorArray
from pyntcloud import PyntCloud
from vispy import app, gloo


class PointCloudCanvas:

    def __init__(self, point_cloud):
        self.point_cloud = point_cloud

        canvas = vispy.scene.SceneCanvas(keys='interactive', show=True)
        view = canvas.central_widget.add_view()

        pos = point_cloud.points[['x', 'y', 'z']].values
        colarr = ColorArray(color=point_cloud.points[['red', 'green', 'blue', 'opacity']].values)

        # create scatter object and fill in the data
        scatter = visuals.Markers()
        scatter.set_data(pos, edge_width=0, face_color=colarr, size=5)

        view.add(scatter)

        view.camera = 'turntable'  # or try 'arcball'

        # add a colored 3D axis for orientation
        self.axis = visuals.XYZAxis(parent=view.scene)

    def run(self):
        vispy.app.run()


if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1:
        canvas.run()