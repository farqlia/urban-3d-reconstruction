from PyQt5.Qt3DExtras import Qt3DWindow, QFirstPersonCameraController
from PySide6.QtGui import QVector3D
from PySide6.QtWidgets import QWidget, QHBoxLayout


class View3D(QWidget):
    def __init__(self):
        super().__init__()
        self.view = Qt3DWindow()
        self.container = self.createWindowContainer(self.view)

        vboxlayout = QHBoxLayout()
        vboxlayout.addWidget(self.container)
        self.setLayout(vboxlayout)

        # put some nodes in the scene
        # scene = createScene()
        # Camera
        camera = self.view.camera()
        camera.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        camera.setPosition(QVector3D(0.0, 0.0, 40.0))
        camera.setViewCenter(QVector3D(0.0, 0.0, 0.0))

        # For camera controls.
        camController = QFirstPersonCameraController(scene)
        camController.setLinearSpeed(50.0)
        camController.setLookSpeed(180.0)
        camController.setCamera(camera)

        # assign root node to the view
        self.view.setRootEntity(scene)