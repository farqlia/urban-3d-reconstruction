from PySide6.QtQml import QQmlEngine
from PySide6.QtCore import QObject, QUrl
from PySide6.QtQuickWidgets import QQuickWidget

from .config import QML_IMPORT

class EngineManager(QObject):
    def __init__(self):
        super().__init__()

        self.engine = QQmlEngine()
        self.engine.addImportPath(QML_IMPORT)
    
    def set_qml_property(self, name, prop):
        self.engine.rootContext().setContextProperty(name, prop)

    def load_component(self, qml_file, parent):
        widget = QQuickWidget(self.engine, parent)
        widget.setSource(QUrl.fromLocalFile(qml_file))
        widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        return widget