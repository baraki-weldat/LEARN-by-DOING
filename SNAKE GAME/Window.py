from PyQt5.QtCore import Qt, QTime, QTimer, QElapsedTimer, QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QFont

import GameWidget


class Timer(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.setGeometry(QRect(0, 60, 200, 40))
        self.elapsed = QElapsedTimer()
        self.elapsed.start()

    def update_timer(self):
        time = QTime.currentTime().toString("hh:mm:ss")
        seconds = str(round(self.elapsed.elapsed()/1000))
        minutes = str(round(self.elapsed.elapsed()/60000))
        hours = str(round(self.elapsed.elapsed()/3600000))
        self.setText(f"Time: {time}.nElapsed: {hours}h {minutes}' {seconds}'")


class UI(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self)
        self.main_window = parent
        self.setWindowTitle("Statistics")
        self.setMinimumSize(200, 200)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.Tool, True)
        font = QFont()
        font.setPointSize(12)
        self.setFont(font)

        central_widget = QWidget()
        self.label_food_count = QLabel("Food count: 0", central_widget, geometry=QRect(0, 0, 200, 20))
        self.label_snake_length = QLabel("Snake length: 3", central_widget, geometry=QRect(0, 20, 200, 20))
        self.label_death_counter = QLabel("Deaths counter: 0", central_widget, geometry=QRect(0, 40, 200, 20))
        self.label_time_elapsed = Timer(central_widget)

        self.setCentralWidget(central_widget)
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("QSnake")

        self.ui = UI(self)
        game_widget = GameWidget.GameWidget(self)
        game_widget.setFocusPolicy(Qt.ClickFocus)

        self.setCentralWidget(game_widget)

        self.setMinimumSize(400, 400)
        self.showMaximized()
