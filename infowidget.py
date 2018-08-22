#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *
from tcpsocket import *

class InfoWidget(QWidget):
    def __init__(self, begin = 0, end = 2, parent=None):# program and single modal just 2 sections to show info
        super().__init__(parent)
        self.begin = begin
        self.end = end
        self.sceneWidgetList = []
        self.singleWidgetList = []
        self.sceneWidgetCount = 0
        self.layout=QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        for i in range(begin, end):
            sw = SceneWidget()
            self.layout.addWidget(sw)
            self.sceneWidgetList.append(sw)
            sw.hide()
        for i in range(begin, end):
            sw = SingleWidget("{}区".format(i+1))
            self.layout.addWidget(sw)
            self.singleWidgetList.append(sw)
        self.setLayout(self.layout)

    def showWidgets(self, info):
        try:
            if len(info) == 4 and info[0] == 2 and info[2] == "value":
                infoValue = info[3]
                if int(infoValue[TcpSocket.Section]) not in range(self.begin, self.end):
                    return
                if infoValue[TcpSocket.Modal] == "Program":
                    sw = self.sceneWidgetList[int(infoValue[TcpSocket.Section])%len(self.sceneWidgetList)]
                    if sw:
                        sw.showDevice(infoValue)
                elif infoValue[TcpSocket.Modal] == "Single":
                    sec = int(infoValue[TcpSocket.Section])%len(self.singleWidgetList)
                    self.singleWidgetList[sec].showDevice(infoValue)
            elif len(info) == 4 and info[0] == 2 and info[2] == "setScreen":
                if not info[3]: # single
                    for sw in self.singleWidgetList:
                        sw.show()
                    for sw in self.sceneWidgetList:
                        sw.hide()
                else:           # program
                    for sw in self.singleWidgetList:
                        sw.hide()
                    for sw in self.sceneWidgetList:
                        sw.show()
        except Exception as e:
            print("showWidgets", e)
class SingleWidget(QFrame):
    MaxRow = 9
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
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.setLayout(self.mainLayout)

    def showDevice(self, info):
        devList = info["Device"]
        try:
            while len(devList) < SingleWidget.MaxRow or len(devList)%SingleWidget.MaxRow:
                devList.append(["",""])
            devWidgetNum = len(devList)//(SingleWidget.MaxRow+1) + 1
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
                    item = QTableWidgetItem(dev[0])
                    item.setTextAlignment(Qt.AlignHCenter)
                    w.setItem(row, 0, item)
                if w.item(row, 1):
                    w.item(row, 1).setText(str(dev[1]))
                else:
                    item = QTableWidgetItem(str(dev[1]))
                    item.setTextAlignment(Qt.AlignHCenter)
                    w.setItem(row, 1, item)
                count += 1
        except Exception as e:
            print(str(e))
    def createTableWidget(self):
        hHeaderLabels = ["名称", "状态"]
        devWidget = QTableWidget()
        devWidget.setSelectionMode(QAbstractItemView.NoSelection)
        devWidget.setFocusPolicy(Qt.NoFocus)
        devWidget.setShowGrid(False)
        devWidget.verticalHeader().setHidden(True)
        devWidget.setColumnCount(len(hHeaderLabels))
        devWidget.setRowCount(SingleWidget.MaxRow)
        devWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        devWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        devWidget.setHorizontalHeaderLabels(hHeaderLabels)
        devWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # devWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        devWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        return devWidget
class SceneWidget(QFrame):
    MaxRow = 9
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = QLabel()
        deviceTableWidget = self.createTableWidget()
        self.devTableWidgetLayout = QHBoxLayout()
        self.devTableWidgetLayout.addWidget(deviceTableWidget)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel, alignment=Qt.AlignHCenter)
        self.mainLayout.addLayout(self.devTableWidgetLayout)
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(0)
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
            self.titleLabel.setText(self.tr("无编场信息"))
        devList = []
        if info["Device"]:
            devList = info["Device"]
        while len(devList) < SceneWidget.MaxRow or len(devList)%SceneWidget.MaxRow:
            devList.append(["", "", "", None, None])
        try:
            devWidgetNum = len(devList)//(SceneWidget.MaxRow+1) + 1
            while self.devTableWidgetLayout.count() > devWidgetNum: # create table Widget according devList
                w = self.devTableWidgetLayout.takeAt(0).widget()
                w.setParent(None)
                del w
            while self.devTableWidgetLayout.count() < devWidgetNum:
                devWidget = self.createTableWidget()
                self.devTableWidgetLayout.addWidget(devWidget)
            count = 0
            for dev in devList:
                w = self.devTableWidgetLayout.itemAt(count//SceneWidget.MaxRow).widget()
                row = count % SingleWidget.MaxRow
                w.item(row, 0).setText(str(dev[0]))
                w.item(row, 1).setText(str(dev[1]))
                w.item(row, 2).setText(str(dev[2]))
                if dev[3] != None:
                    w.cellWidget(row, 3).layout().itemAt(0).widget().setVisible(True)
                    w.cellWidget(row, 3).layout().itemAt(0).widget().setChecked(dev[3])
                else:
                    w.cellWidget(row, 3).layout().itemAt(0).widget().setVisible(False)
                if dev[4] != None:
                    w.cellWidget(row, 4).layout().itemAt(0).widget().setVisible(True)
                    w.cellWidget(row, 4).layout().itemAt(0).widget().setChecked(dev[4])
                else:
                    w.cellWidget(row, 4).layout().itemAt(0).widget().setVisible(False)
                count += 1
        except Exception as e:
            print("SceneWidget show device", str(e))

    def createTableWidget(self):
        deviceTableWidget = QTableWidget()
        deviceTableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        deviceTableWidget.setFocusPolicy(Qt.NoFocus)
        hHeaderLabels = ["名称", "位置", "速度", "上限", "下限"]
        deviceTableWidget.setColumnCount(len(hHeaderLabels))
        deviceTableWidget.setHorizontalHeaderLabels(hHeaderLabels)
        deviceTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        deviceTableWidget.verticalHeader().setHidden(True)
        # deviceTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        deviceTableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        deviceTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.deviceTableWidget.verticalHeader().setDefaultSectionSize()
        deviceTableWidget.setShowGrid(False)
        deviceTableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        deviceTableWidget.setRowCount(SceneWidget.MaxRow)
        for row in range(SceneWidget.MaxRow):  # name pos speed uplimit downlimit
            devNameItem = QTableWidgetItem()
            devNameItem.setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            deviceTableWidget.setItem(row, 0, devNameItem)
            posItem = QTableWidgetItem()
            posItem.setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
            deviceTableWidget.setItem(row, 1, posItem)
            speedItem = QTableWidgetItem()
            speedItem.setTextAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
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
