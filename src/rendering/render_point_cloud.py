import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from PySide6.QtOpenGLWidgets import QOpenGLWidget


class PointCloudGLWidget(QOpenGLWidget):
    def __init__(self, point_cloud=None, parent=None):
        super(PointCloudGLWidget, self).__init__(parent)
        self.point_cloud = point_cloud if point_cloud is not None else np.zeros((0, 3))

        # Initial camera rotation and zoom values
        self.x_rot = 0
        self.y_rot = 0
        self.zoom = -10  # Initial zoom level (distance from the object)
        self.last_mouse_pos = None  # Track the last mouse position for dragging

    def initializeGL(self):
        """Initialize OpenGL settings."""
        glEnable(GL_DEPTH_TEST)
        glPointSize(3)
        glClearColor(0.1, 0.1, 0.1, 1.0)

    def resizeGL(self, width, height):
        """Handle resizing of the OpenGL window."""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Render the point cloud."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, self.zoom)  # Apply the zoom (camera distance)

        # Apply rotations based on mouse interactions
        glRotatef(self.x_rot, 1.0, 0.0, 0.0)  # Rotate around the X-axis
        glRotatef(self.y_rot, 0.0, 1.0, 0.0)  # Rotate around the Y-axis

        self.draw_point_cloud()

    def draw_point_cloud(self):
        # Draw the point cloud
        glBegin(GL_POINTS)
        for (i, p) in self.point_cloud.iterrows():
            glColor3f(p['red'], p['green'], p['blue'])
            glVertex3f(p['x'], p['y'], p['z'])
        glEnd()

    def mousePressEvent(self, event):
        """Capture the initial mouse position when the mouse button is pressed."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.position()

    def mouseMoveEvent(self, event):
        """Update rotation angles based on mouse movement."""
        if self.last_mouse_pos is not None:
            dx = event.position().x() - self.last_mouse_pos.x()
            dy = event.position().y() - self.last_mouse_pos.y()

            # Update rotation angles: modify the scale to control sensitivity
            self.x_rot += dy * 0.5
            self.y_rot += dx * 0.5

            # Save the new mouse position
            self.last_mouse_pos = event.position()

            # Trigger a redraw
            self.update()

    def mouseReleaseEvent(self, event):
        """Clear the last mouse position when the mouse button is released."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = None

    def wheelEvent(self, event):
        """Handle mouse wheel events for zooming."""
        delta = event.angleDelta().y()
        zoom_step = 0.2  # Adjust zoom speed here

        # Increase zoom (move closer) if scrolling up, and decrease (move away) if scrolling down
        if delta > 0:
            self.zoom += zoom_step
        else:
            self.zoom -= zoom_step

        # Trigger a redraw
        self.update()

    def setPointCloud(self, point_cloud):
        """Update the point cloud data."""
        self.point_cloud = point_cloud
        self.update()


class MainWindow(QMainWindow):
    def __init__(self, point_cloud):
        super(MainWindow, self).__init__()
        self.setWindowTitle("3D Point Cloud Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Instantiate PointCloudGLWidget and set it as the central widget
        self.gl_widget = PointCloudGLWidget(point_cloud)
        self.setCentralWidget(self.gl_widget)


def generate_random_point_cloud(num_points=1000, scale=10):
    """Generate a random point cloud for demonstration."""
    return np.random.rand(num_points, 3) * scale - (scale / 2)


def prepare_point_cloud(point_cloud):
    point_cloud.points['red'] = point_cloud.points['red'] / 255.0
    point_cloud.points['green'] = point_cloud.points['green'] / 255.0
    point_cloud.points['blue'] = point_cloud.points['blue'] / 255.0
