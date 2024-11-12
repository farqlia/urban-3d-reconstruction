from PySide6.QtCore import QThread, Signal, QRunnable, QObject
import time

class BasicThreadScript(QRunnable):
    def __init__(self, func, callback):
        super().__init__()
        self._func = func
        self._callback = callback

    def run(self):
        result = self._func()
        self._callback(result)