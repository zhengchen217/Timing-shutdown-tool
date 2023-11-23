import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QDateTimeEdit
from PyQt6.QtCore import QTimer, QDateTime
import subprocess
import platform

class ShutdownTimerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 初始化用户界面
        self.setWindowTitle('定时关机')

        # 布局设置
        self.mainLayout = QVBoxLayout()
        self.dateTimeLayout = QHBoxLayout()
        self.countdownLayout = QHBoxLayout()

        # 日期和时间选择器，用于设置具体时间关机
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        self.dateTimeLayout.addWidget(QLabel('日期和时间:'))
        self.dateTimeLayout.addWidget(self.dateTimeEdit)

        # 设置具体时间关机按钮
        self.setSpecificTimeBtn = QPushButton('设置具体时间关机', self)
        self.setSpecificTimeBtn.clicked.connect(self.setSpecificTimeShutdown)

        # 小时和分钟选择器，用于设置倒计时关机
        self.hourSpin = QSpinBox()
        self.hourSpin.setRange(0, 23)
        self.minuteSpin = QSpinBox()
        self.minuteSpin.setRange(0, 59)

        self.countdownLayout.addWidget(QLabel('小时:'))
        self.countdownLayout.addWidget(self.hourSpin)
        self.countdownLayout.addWidget(QLabel('分钟:'))
        self.countdownLayout.addWidget(self.minuteSpin)

        # 设置倒计时关机按钮
        self.setCountdownBtn = QPushButton('设置倒计时关机', self)
        self.setCountdownBtn.clicked.connect(self.setCountdownShutdown)

        # 倒计时显示标签
        self.countdownLabel = QLabel('')

        # 将小部件添加到主布局
        self.mainLayout.addLayout(self.dateTimeLayout)
        self.mainLayout.addWidget(self.setSpecificTimeBtn)
        self.mainLayout.addLayout(self.countdownLayout)
        self.mainLayout.addWidget(self.setCountdownBtn)
        self.mainLayout.addWidget(self.countdownLabel)
        self.setLayout(self.mainLayout)

    def setSpecificTimeShutdown(self):
        # 设置具体时间关机
        shutdown_datetime = self.dateTimeEdit.dateTime()
        current_datetime = QDateTime.currentDateTime()

        self.seconds = shutdown_datetime.toSecsSinceEpoch() - current_datetime.toSecsSinceEpoch()
        self.startCountdown()

    def setCountdownShutdown(self):
        # 设置倒计时关机
        hours = self.hourSpin.value()
        minutes = self.minuteSpin.value()
        self.seconds = hours * 3600 + minutes * 60
        self.startCountdown()

    def startCountdown(self):
        # 开始倒计时
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCountdown)
        self.timer.start(1000)

    def updateCountdown(self):
        # 更新倒计时显示
        if self.seconds > 0:
            days, remainder = divmod(self.seconds, 86400)
            hours, remainder = divmod(remainder, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.countdownLabel.setText(f'距离关机时间还有: {days}天{hours:02}小时{minutes:02}分钟{seconds:02}秒')
            self.seconds -= 1
        else:
            self.timer.stop()
            self.shutdown()

    def shutdown(self):
        # 执行关机操作
        os_type = platform.system()
        try:
            if os_type == "Windows":
                subprocess.run(["shutdown", "/s", "/t", str(0)])
            elif os_type == "Linux" or os_type == "Darwin":
                subprocess.run(["shutdown", "-h", "now"])
        except Exception as e:
            print("关机过程中出错:", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShutdownTimerApp()
    ex.show()
    sys.exit(app.exec())
