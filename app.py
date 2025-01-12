import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFileDialog,
)
from PyQt5.QtCore import QThread, pyqtSignal
import pyautogui
import time


class ScreenRecorder(QThread):
    status_signal = pyqtSignal(str)  # To update status in GUI

    def __init__(self, save_path):
        super().__init__()
        self.save_path = save_path
        self.recording = False

    def run(self):
        self.recording = True
        self.status_signal.emit("Recording started...")

        screen_size = pyautogui.size()  # Get screen resolution
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.save_path, fourcc, 20.0, screen_size)

        while self.recording:
            img = pyautogui.screenshot()  # Capture screen
            frame = np.array(img)  # Convert to numpy array
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to OpenCV format
            out.write(frame)  # Write frame to video file
            time.sleep(0.05)  # Adjust for frame rate

        out.release()
        self.status_signal.emit("Recording stopped.")

    def stop(self):
        self.recording = False
        self.quit()


class ScreenRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.recorder = None
        self.save_path = "output.avi"  # Default save path

    def initUI(self):
        self.setWindowTitle("Screen Recorder - Developed by KAMRUL MOLLAH")
        self.setGeometry(200, 200, 400, 250)

        # Layout and widgets
        layout = QVBoxLayout()
        self.status_label = QLabel("Status: Ready", self)
        self.start_button = QPushButton("Start Recording", self)
        self.stop_button = QPushButton("Stop Recording", self)
        self.browse_button = QPushButton("Browse Save Path", self)
        self.quit_button = QPushButton("Quit", self)

        # Developer info
        developer_label = QLabel("Developed by: KAMRUL MOLLAH", self)
        developer_label.setOpenExternalLinks(True)

        layout.addWidget(self.status_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.quit_button)
        layout.addWidget(developer_label)  # Add developer info

        # Main widget
        main_widget = QWidget(self)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        # Button actions
        self.start_button.clicked.connect(self.start_recording)
        self.stop_button.clicked.connect(self.stop_recording)
        self.browse_button.clicked.connect(self.browse_save_path)
        self.quit_button.clicked.connect(self.close)

    def start_recording(self):
        if not self.recorder:
            self.recorder = ScreenRecorder(self.save_path)
            self.recorder.status_signal.connect(self.update_status)
            self.recorder.start()

    def stop_recording(self):
        if self.recorder:
            self.recorder.stop()
            self.recorder = None

    def browse_save_path(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Video Files (*.avi);;All Files (*)", options=options
        )
        if file_path:
            self.save_path = file_path
            self.update_status(f"Save path set to: {self.save_path}")

    def update_status(self, message):
        self.status_label.setText(f"Status: {message}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScreenRecorderApp()
    window.show()
    sys.exit(app.exec_())
