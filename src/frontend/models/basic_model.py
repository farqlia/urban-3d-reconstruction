from PySide6.QtCore import Slot, QObject, Property, Signal, QUrl

class BasicModelStr(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._data = ""

    @Property(str, notify=dataChanged)
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

    
class BasicModelList(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._data = []

    @Property('QVariantList', notify=dataChanged)
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

class BasicModelInt(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._data = 0

    @Property(int, notify=dataChanged)
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()