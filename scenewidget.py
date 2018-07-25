#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *
from tcpsocket import *

class DevWidget(QWidget):
    def __init__(self, number=2, parent=None):
        super().__init__(parent)
        self.sceneWidgetList = []
        self.singleWidgetList = []
        self.sceneWidgetCount = 0
        self.layout=QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        for i in range(number):
            sw = SceneWidget()
            self.layout.addWidget(sw)
            self.sceneWidgetList.append(sw)
        for i in range(number):
            id = int(Config.value(Config.monitorId))
            sw = SingleWidget("{}区".format((id%2)*2+1+i))
            self.layout.addWidget(sw)
            self.singleWidgetList.append(sw)
        self.setLayout(self.layout)

    def showWidgets(self, info):
        try:
            if info[TcpSocket.Modal] == "Program":
                for sw in self.singleWidgetList:
                    sw.hide()
                for sw in self.sceneWidgetList:
                    sw.show()
                sw = self.sceneWidgetList[self.sceneWidgetCount]
                if sw:
                    sw.showDevice(info)
                self.sceneWidgetCount += 1
                self.sceneWidgetCount %= len(self.sceneWidgetList)
            elif info[TcpSocket.Modal] == "Single":
                for sw in self.singleWidgetList:
                    sw.show()
                for sw in self.sceneWidgetList:
                    sw.hide()
                sec = int(info[TcpSocket.Section])%2
                self.singleWidgetList[sec].showDevice(info["Device"])
        except Exception as e:
            print("showWidgets", e)
class SingleWidget(QWidget):
    MaxRow = 10
    def __init__(self, name, parent=None):
        super().__init__(parent)
        self.titleLabel = QLabel(name)
        self.titleLabel.setAlignment(Qt.AlignHCenter)
        self.titleLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.devWidgetLayout = QHBoxLayout()
        devWidget = self.createTableWidget()
        self.devWidgetLayout.addWidget(devWidget)
        self.devWidgetLayout.setContentsMargins(0,0,0,0)
        self.devWidgetLayout.setSpacing(0)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addLayout(self.devWidgetLayout)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)

    def showDevice(self, dev):
        try:
            devList = dev
            devWidgetNum = len(devList)//10 + 1
            while self.devWidgetLayout.count() > devWidgetNum:
                w = self.devWidgetLayout.takeAt(0).widget()
                w.setParent(None)
                del w
            while self.devWidgetLayout.count() < devWidgetNum:
                devWidget = self.createTableWidget()
                self.devWidgetLayout.addWidget(devWidget)
            count = 0
            for dev in devList:
                w = self.devWidgetLayout.itemAt(count//SingleWidget.MaxRow).widget()
                row = count % SingleWidget.MaxRow
                if w.item(row, 0):
                    w.item(row, 0).setText(dev[0])
                else:
                    w.setItem(row, 0, QTableWidgetItem(dev[0]))
                if w.item(row, 1):
                    w.item(row, 1).setText(str(dev[1]))
                else:
                    w.setItem(row, 1, QTableWidgetItem(str(dev[1])))
                count += 1
        except Exception as e:
            print(str(e))
    def createTableWidget(self):
        hHeaderLabels = ["设备名称", "状态"]
        devWidget = QTableWidget()
        devWidget.setShowGrid(False)
        devWidget.verticalHeader().setHidden(True)
        devWidget.setColumnCount(len(hHeaderLabels))
        devWidget.setRowCount(SingleWidget.MaxRow)
        devWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        devWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        devWidget.setHorizontalHeaderLabels(hHeaderLabels)
        devWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        devWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        return devWidget
class SceneWidget(QWidget):
    MaxRow = 10
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = QLabel()
        deviceTableWidget = self.createTableWidget()
        self.devTableWidgetLayout = QHBoxLayout()
        self.devTableWidgetLayout.addWidget(deviceTableWidget)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel, alignment=Qt.AlignHCenter)
        self.mainLayout.addLayout(self.devTableWidgetLayout)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(self.mainLayout)
        # while True:
        #     self.showDevice(info=None)
    def clearTableWidget(self):
        for row in range(self.deviceTableWidget.rowCount()):
            for col in range(self.deviceTableWidget.columnCount()):
                item = self.deviceTableWidget.cellWidget(row, col)
                if isinstance(item, QWidget):
                    item.setParent(None)
                    del item
                else:
                    item = self.deviceTableWidget.takeItem(row, col)
                    if item:
                        del item
        self.deviceTableWidget.clearContents()

    def showDevice(self, info): # name, pos, speed, uplimit, downlimit
        # self.clearTableWidget()
        sceneName = info["SceneName"] if info["SceneName"] else ""
        if info["PlayName"]:
            self.titleLabel.setText("{}:({})".format(sceneName, info["PlayName"]))
        else:
            self.titleLabel.setText("")
        if not info["Device"]:
            return
        devList = info["Device"]
        try:
            devWidgetNum = len(devList)//SceneWidget.MaxRow + 1
            while self.devTableWidgetLayout.count() > devWidgetNum:
                w = self.devTableWidgetLayout.takeAt(0).widget()
                w.setParent(None)
                del w
            while self.devTableWidgetLayout.count() < devWidgetNum:
                devWidget = self.createTableWidget()
                self.devTableWidgetLayout.addWidget(devWidget)
            count = 0
            for dev in devList:
                w = self.devTableWidgetLayout.itemAt(count//SingleWidget.MaxRow).widget()
                row = count % SingleWidget.MaxRow
                w.item(row, 0).setText(str(dev[0]))
                w.item(row, 1).setText(str(dev[1]))
                w.item(row, 2).setText(str(dev[2]))
                w.cellWidget(row, 3).layout().itemAt(0).widget().setVisible(True)
                w.cellWidget(row, 4).layout().itemAt(0).widget().setVisible(True)
                count += 1
        except Exception as e:
            print(str(e))

    def createTableWidget(self):
        deviceTableWidget = QTableWidget()
        hHeaderLabels = ["设备名称", "位置", "速度", "上限", "下限"]
        deviceTableWidget.setColumnCount(len(hHeaderLabels))
        deviceTableWidget.setHorizontalHeaderLabels(hHeaderLabels)
        deviceTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        deviceTableWidget.verticalHeader().setHidden(True)
        deviceTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        deviceTableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        deviceTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.deviceTableWidget.verticalHeader().setDefaultSectionSize()
        deviceTableWidget.setShowGrid(False)
        deviceTableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        deviceTableWidget.setRowCount(SceneWidget.MaxRow)
        for row in range(SceneWidget.MaxRow):  # name pos speed uplimit downlimit
            devNameItem = QTableWidgetItem()
            devNameItem.setTextAlignment(Qt.AlignHCenter)
            deviceTableWidget.setItem(row, 0, devNameItem)
            posItem = QTableWidgetItem()
            posItem.setTextAlignment(Qt.AlignHCenter)
            deviceTableWidget.setItem(row, 1, posItem)
            speedItem = QTableWidgetItem()
            speedItem.setTextAlignment(Qt.AlignHCenter)
            deviceTableWidget.setItem(row, 2, speedItem)
            upRadioButton = QRadioButton()
            upRadioButton.setChecked(0)
            upRadioButton.setVisible(False)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(upRadioButton, alignment=Qt.AlignHCenter)
            layout.setContentsMargins(0,0,0,0)
            widget.setLayout(layout)
            deviceTableWidget.setCellWidget(row, 3, widget)
            downRadioButton = QRadioButton()
            downRadioButton.setChecked(0)
            downRadioButton.setVisible(False)
            widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(downRadioButton, alignment=Qt.AlignHCenter)
            layout.setContentsMargins(0,0,0,0)
            widget.setLayout(layout)
            deviceTableWidget.setCellWidget(row, 4, widget)
        return deviceTableWidget
