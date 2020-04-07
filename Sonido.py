from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
import sys
from PyQt5.QtCore import QUrl, QCoreApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class sound(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hola")
        self.sound = Sounds()
        self.initwindow()

    def initwindow(self):
        vbox = QVBoxLayout()
        button = QPushButton()
        button.clicked.connect(self.play)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def play(self):
        self.sound.start()

class Sounds():
    def __init__(self):
        self.player = QMediaPlayer()
        self.sounds = {'Start': "Sounds/Start_Windows.wav"}

    def start(self):
        self.player.setMedia(QMediaContent(QUrl(self.sounds['Start'])))
        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = sound()
    window.show()
    app.exec()