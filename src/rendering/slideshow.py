from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QPixmap
import os


class SlideshowWidget(QWidget):
    def __init__(self, folder_path, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.image_files = self._get_image_files(folder_path)
        self.current_index = 0

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumSize(600,450)
        self.image_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.image_label.setStyleSheet("border: 1px solid black;")
        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)
        self.play_button = QPushButton("Play", self)
        self.stop_button = QPushButton("Stop", self)

        self.prev_button.clicked.connect(self.show_previous_image)
        self.next_button.clicked.connect(self.show_next_image)
        self.play_button.clicked.connect(self.start_slideshow)
        self.stop_button.clicked.connect(self.stop_slideshow)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.prev_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.play_button)
        button_layout.addWidget(self.stop_button)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addLayout(button_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_image)

        self.show_image(0)

    def _get_image_files(self, folder):
        return [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

    def show_image(self, index):
        if self.image_files:
            file_path = os.path.join(self.folder_path, self.image_files[index])
            pixmap = QPixmap(file_path)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def show_next_image(self):
        if self.image_files:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.show_image(self.current_index)

    def show_previous_image(self):
        if self.image_files:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.show_image(self.current_index)

    def start_slideshow(self):
        self.timer.start(2000)

    def stop_slideshow(self):
        self.timer.stop()
