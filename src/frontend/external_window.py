from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import subprocess
import ctypes
import sys

def external_window(window_id):
    window_id = int(window_id)

    external_window = QWindow.fromWinId(window_id)
    
    if external_window is None:
        return QWindow()

    external_window.setFlags(Qt.FramelessWindowHint)

    return external_window


if __name__ == "__main__":
    windowIdStr = subprocess.check_output(['sh', '-c', r"xwininfo -int | sed -ne 's/.*Window id: \([0-9a-fA-Fx]\+\).*/\1/p'"]).decode('utf-8')
    windowId = int(windowIdStr)
    print(windowId)
    # app = QApplication(sys.argv)
    # mainWindow = QMainWindow()
    # mainWindow.show()

    # externalWindow = QWindow.fromWinId(windowId)
    # externalWindow.setFlags(Qt.FramelessWindowHint)
    # container = QWidget.createWindowContainer(externalWindow)
    # mainWindow.setCentralWidget(container)