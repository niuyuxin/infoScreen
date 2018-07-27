#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from ui import ui_mainwindow
from PyQt5.QtCore import *
from infowidget import *
from tcpsocket import *

class MainWindow(QWidget, ui_mainwindow.Ui_mainwindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.rtcTimer = QTimer()
        self.rtcTimer.timeout.connect(self.onRtcTimerTimeout)
        self.rtcTimer.start(1000)
        self.setFixedSize(1920, 360)
        self.dateTimeLayout.setAlignment(self.timeLabel, Qt.AlignHCenter)
        self.dateTimeLayout.setAlignment(self.weekLabel, Qt.AlignHCenter)
        self.dateTimeLayout.setAlignment(self.dateLabel, Qt.AlignHCenter)
        self.onRtcTimerTimeout()
        # create tcp socket
        self.tcpSocket = TcpSocket()
        self.tcpSocketThread = QThread()
        self.tcpSocket.moveToThread(self.tcpSocketThread)
        self.tcpSocketThread.started.connect(self.tcpSocket.initTcpSocket)
        self.tcpSocketThread.start()

        self.contentLayout = QHBoxLayout()
        widget = InfoWidget()
        self.tcpSocket.modalChanged.connect(widget.showWidgets)
        self.contentLayout.addWidget(widget)

        self.contentLayout.setContentsMargins(0,0,0,0)
        self.contentFrame.setLayout(self.contentLayout)

    def onRtcTimerTimeout(self):
        dtStr = QDateTime.currentDateTime().toString("yyyy年MM月dd日 hh:mm:ss dddd")
        dataStr, timeStr, weekStr = dtStr.split(" ")
        self.timeLabel.setText(timeStr)
        self.weekLabel.setText(weekStr)
        self.dateLabel.setText(dataStr)
