import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import Slot, QObject, Property, Signal, QUrl
from PySide6.QtWidgets import QFileDialog

class Backend(QObject):
    directoryPathChanged = Signal()
    fileListChanged = Signal()

    def __init__(self):
        super().__init__()
        self._directory_path = ""
        self._file_list = []

    @Property(str, notify=directoryPathChanged)
    def directoryPath(self):
        return self._directory_path

    @directoryPath.setter
    def directoryPath(self, path):
        dir_path = QUrl(path).toLocalFile()
        if self._directory_path != dir_path:
            self._directory_path = dir_path
            self.directoryPathChanged.emit()
            self.fileList = [f for f in os.listdir(self._directory_path) if os.path.isfile(os.path.join(self._directory_path, f))]

    @Property('QVariantList', notify=fileListChanged)
    def fileList(self):
        return self._file_list

    @fileList.setter
    def fileList(self, files):
        if self._file_list != files:
            self._file_list = files
            self.fileListChanged.emit()

    @Slot()
    def generatePointCloud(self):
        pass

    @Slot()
    def generateSplats(self):
        pass

    @Slot()
    def categorize(self):
        pass

    @Slot()
    def progress_value(self):
        return 50.0

if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = Backend()

    engine.rootContext().setContextProperty("backend", backend)

    engine.addImportPath(sys.path[0])
    engine.loadFromModule("Main", "MainWindow")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
