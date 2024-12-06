from pathlib import Path
import os
from dotenv import load_dotenv
from sys import platform

QML_IMPORT = "src/frontend/views"
HEADER_FILE = "src/frontend/views/Main/Header.qml"
FOOTER_FILE = "src/frontend/views/Main/Footer.qml"
LEFT_PANE_FILE = "src/frontend/views/Main/BodyLeftPane.qml"
LOADING_WINDOW_FILE = "src/frontend/views/Main/LoadingWindow.qml"
SUCC_WINDOW_FILE = "src/frontend/views/Main/SuccessWindow.qml"
FAIL_WINDOW_FILE = "src/frontend/views/Main/ErrorWindow.qml"
SETTINGS_WINDOW = "src/frontend/views/Main/SettingsWindow.qml"
RIGHT_PANE_LT_FILE = "src/frontend/views/Main/BodyRightPaneLT.qml"
RIGHT_PANE_RT_FILE = "src/frontend/views/Main/BodyRightPaneRT.qml"
RIGHT_PANE_LB_FILE = "src/frontend/views/Main/BodyRightPaneLB.qml"
RIGHT_PANE_RB_FILE = "src/frontend/views/Main/BodyRightPaneRB.qml"