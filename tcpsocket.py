#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtNetwork import *
from PyQt5.QtCore import *
from config import *
import collections
import ast
import json
class TcpSocket(QObject):
    Modal = "Modal"
    Section = "Section"
    tcpState=pyqtSignal(int)
    modalChanged = pyqtSignal(dict)
    def __init__(self, parent=None):
        super().__init__(parent)

    @pyqtSlot()
    def initTcpSocket(self):
        self.tcpSocket = QTcpSocket(self)
        self.tcpSocket.connected.connect(self.onTcpSocketConnected)
        self.tcpSocket.readyRead.connect(self.onTcpSocketReadyRead)
        self.tcpSocket.disconnected.connect(self.onTcpSocketDisconnected)
        self.tcpSocket.error.connect(self.onTcpSocketError)
        self.connectTimer = QTimer(self)
        self.connectTimer.timeout.connect(self.connectServer, Qt.DirectConnection)
        self.connectTimer.start(1000)
    @pyqtSlot()
    def onTcpSocketConnected(self):
        print("Tcp socket connected")
        self.tcpState.emit(self.tcpSocket.state())
        self.connectTimer.stop()
    def sendData(self, data):
        if self.tcpSocket.state() == QAbstractSocket.ConnectedState:
            self.tcpSocket.write(data)
            self.tcpSocket.waitForBytesWritten()
        else:
            print("网络不可用")
    @pyqtSlot()
    def connectServer(self):
        if self.tcpSocket.state() == QAbstractSocket.UnconnectedState:
            ip = Config.value(Config.serverIp)
            if ip == None:
                socketIp = QHostAddress(QHostAddress.LocalHost)  # "192.168.1.177"
            else:
                socketIp = ip
            self.tcpSocket.connectToHost(QHostAddress(socketIp), 5000)
        elif self.tcpSocket.state() == QAbstractSocket.ConnectingState:
            self.tcpState.emit(self.tcpSocket.state())
    @pyqtSlot()
    def onTcpSocketReadyRead(self):
        try:
            temp = self.tcpSocket.readAll()
            serverData = str(temp, encoding="utf-8")
            # print("Get server data:", temp, QDateTime.currentDateTime().toString("hh:mm:ss zzz"))
            if "Hello" in serverData:
                di = {"MonitorName":"infoScreen",
                      "MonitorId":Config.value(Config.monitorId),
                      "MonitorHoldDevice":""
                      }
                self.tcpSocket.write(QByteArray(bytes(str(di), encoding="utf-8")))
                self.tcpSocket.waitForBytesWritten()
            else:
                for dat in serverData.split("\n"):
                    if dat:
                        dataDict = json.loads(dat, encoding='UTF-8')
                        self.modalChanged.emit(dataDict)
        except Exception as e:
            print("onTcpSocketReadyRead", str(e))
    @pyqtSlot()
    def onTcpSocketDisconnected(self):
        print("Tcp socket disconnected")
        self.connectTimer.start(1000)
    @pyqtSlot(QAbstractSocket.SocketError)
    def onTcpSocketError(self, err):
        # print("Tcp Socket error", err)
        self.tcpSocket.close()
        self.connectTimer.start(1000)



