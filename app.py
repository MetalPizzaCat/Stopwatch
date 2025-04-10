import sys, os
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer, Qt, QTime, QElapsedTimer, QTimerEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget, QFileDialog, QHBoxLayout

basedir = os.path.dirname(__file__)

class StopwatchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goblin stopwatch")
        self.time = QTime(0,0)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        buttons = QHBoxLayout()

        start_button = QPushButton("Start")
        stop_button = QPushButton("Stop")
        pause_button = QPushButton("Pause")
        buttons.addWidget(start_button)
        buttons.addWidget(stop_button)
        buttons.addWidget(pause_button)

        start_button.clicked.connect(self.start_timer)
        stop_button.clicked.connect(self.stop_timer)
        pause_button.clicked.connect(self.pause_timer)

        btn_widget = QWidget()
        btn_widget.setLayout(buttons)

        layout = QVBoxLayout()
        layout.addWidget(self.time_label)
        layout.addWidget(btn_widget)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.timer = QElapsedTimer()
        self.timer_id = -1
        self.accumulator = 0
        self._show_time()
        

    def _show_time(self):
        self.time_label.setText(self.time.toString("hh:mm:ss.zzz"))

    def _update_timer(self):
        self.time.addSecs(1)
        self._show_time()

    def start_timer(self):
        self.accumulator = 0
        self.timer.restart()
        if self.timer_id == -1:
            self.timer_id = self.startTimer(50)
        self._show_time()


    def timerEvent(self, ev : QTimerEvent):
        if ev.timerId() != self.timer_id:
            return super().timerEvent(ev)
        time = QTime(0,0)
        time = time.addMSecs(self.accumulator)
        if self.timer.isValid():
            time = time.addMSecs(self.timer.elapsed())
        else:
            self.killTimer(self.timer_id)
            self.timer_id = -1
        self.time = time
        self._show_time()
    
    def stop_timer(self):
        self.time = QTime(0,0)
        self.timer.invalidate()
        self.killTimer(self.timer_id)
        self.timer_id = -1
        self._show_time()

    def pause_timer(self):
        if self.timer.isValid():
            self.accumulator += self.timer.elapsed()
            self.timer.invalidate()
        else:
            self.timer.restart()
            self.timer_id = self.startTimer(50)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(os.path.join(basedir, "stopwatch_icon.svg")))
    window = StopwatchWindow()
    window.show()
    app.exec()
