import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap, QPalette, QColor
import sys

class HandGestureUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hand Gesture")
        self.setGeometry(100, 100, 1280, 720)  # Adjust the window size as needed

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.start_button = QPushButton("Start Capture", self)
        self.start_button.clicked.connect(self.start_capture)
        self.layout.addWidget(self.start_button)

        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.quit_app)
        self.layout.addWidget(self.quit_button)

        self.label = QLabel(self)
        self.layout.addWidget(self.label)

        self.central_widget.setLayout(self.layout)

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)  # Adjust the video resolution as needed
        self.cap.set(4, 720)

        self.detector = HandDetector(detectionCon=0.7, maxHands=2)
        self.keyboard = Controller()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.capture = False

    def start_capture(self):
        if not self.capture:
            self.capture = True
            self.start_button.setText("Stop Capture")
            self.timer.start(30)  # Update frame every 30 milliseconds
        else:
            self.capture = False
            self.start_button.setText("Start Capture")
            self.timer.stop()

    def update_frame(self):
        ret, img = self.cap.read()
        hands, img = self.detector.findHands(img)
        if hands:
            fingers = self.detector.fingersUp(hands[0])
            if fingers == [0, 0, 0, 0, 0]:
                self.keyboard.press(Key.left)
                self.keyboard.release(Key.right)
            elif fingers == [1, 1, 1, 1, 1]:
                self.keyboard.press(Key.right)
                self.keyboard.release(Key.left)
        else:
            self.keyboard.release(Key.left)
            self.keyboard.release(Key.right)

        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_BGR888)
        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)

    def quit_app(self):
        self.cap.release()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HandGestureUI()

    # Set UI background color and label background color
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Blue background
    palette.setColor(QPalette.WindowText, Qt.white)
    window.setPalette(palette)

    # Set title font and style
    window.setWindowTitle("Hand Gesture Recognition - UI")
    window.setStyleSheet("font: 18pt Arial Bold;")

    window.show()
    sys.exit(app.exec_())
