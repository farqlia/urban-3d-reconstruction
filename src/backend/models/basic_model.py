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

class BasicModelBool(QObject):
    dataChanged = Signal()

    def __init__(self, initial_value=False):
        super().__init__()
        self._data = initial_value

    @Property(bool, notify=dataChanged)
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        if self._data != value:
            self._data = value
            self.dataChanged.emit()

class BasicModelFunc(QObject):
    def __init__(self, func):
        super().__init__()
        self.func = func
    
    @Slot()
    def func(self):
        func()