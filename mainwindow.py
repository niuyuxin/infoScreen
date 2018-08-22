#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from ui import ui_mainwindow
from PyQt5.QtCore import *
from infowidget import *
from tcpsocket import *
from config import *

class MainWindow(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        # create tcp socket
        self.subWindowList = []
        sectionSize = int(Config.value(Config.SectionSize))
        for s in range(sectionSize):
            subWindow = SubWindow(s*2, s*2+2)
            self.subWindowList.append(subWindow)
        self.tcpSocket = TcpSocket(mid=Config.value(Config.monitorId))
        self.tcpSocketThread = QThread()
        self.tcpSocket.moveToThread(self.tcpSocketThread)
        self.tcpSocketThread.started.connect(self.tcpSocket.initTcpSocket)
        count = 0
        for window in self.subWindowList:
            if count == 1:
                window.move(1920+1280, 0)
            count += 1
            self.tcpSocket.receivedData.connect(window.receivedData)
        self.tcpSocketThread.start()

class SubWindow(QWidget, ui_mainwindow.Ui_mainwindow):
    receivedData = pyqtSignal(list)
    def __init__(self, begin=0, end=2, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setCursor(Qt.BlankCursor)
        self.setWindowTitle("infoScreen({}-{})".format(begin+1, end))
        self.rtcTimer = QTimer(self)
        self.rtcTimer.timeout.connect(self.onRtcTimerTimeout)
        self.rtcTimer.start(1000)
        self.setFixedSize(1920, 360)
        self.dateTimeLayout.setAlignment(self.timeLabel, Qt.AlignHCenter)
        self.dateTimeLayout.setAlignment(self.weekLabel, Qt.AlignHCenter)
        self.dateTimeLayout.setAlignment(self.dateLabel, Qt.AlignHCenter)
        self.onRtcTimerTimeout()
        self.contentLayout = QHBoxLayout()
        widget = InfoWidget(begin, end)
        self.receivedData.connect(widget.showWidgets)
        self.contentLayout.addWidget(widget)
        self.contentLayout.setContentsMargins(0,0,0,0)
        self.contentFrame.setLayout(self.contentLayout)
        self.show()

    def onRtcTimerTimeout(self):
        dtStr = QDateTime.currentDateTime().toString("yyyy年MM月dd日 hh:mm:ss dddd")
        dataStr, timeStr, weekStr = dtStr.split(" ")
        self.timeLabel.setText(timeStr)
        self.weekLabel.setText(weekStr)
        self.dateLabel.setText(dataStr)
