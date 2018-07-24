#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *

class SceneWidgets(QWidget):
    def __init__(self, number=2, parent=None):
        super().__init__(parent)
        self.sceneWidgetList = []
        self.sceneWidgetCount = 0
        self.layout=QHBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        for i in range(number):
            sw = SceneWidget()
            self.layout.addWidget(sw)
            self.sceneWidgetList.append(sw)
        self.setLayout(self.layout)
    def showWidgets(self, info):
        sw = self.sceneWidgetList[self.sceneWidgetCount]
        if sw:
            sw.showDevice(info)
        self.sceneWidgetCount += 1
        self.sceneWidgetCount %= len(self.sceneWidgetList)

class SceneWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = QLabel()
        self.deviceTableWidget = QTableWidget()
        self.deviceTableWidget.setColumnCount(5)
        hHeaderLabels = ["设备名称", "位置", "速度", "上限", "下限"]
        self.deviceTableWidget.setHorizontalHeaderLabels(hHeaderLabels)
        self.deviceTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.deviceTableWidget.verticalHeader().setHidden(True)
        self.deviceTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.deviceTableWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.deviceTableWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.deviceTableWidget.verticalHeader().setDefaultSectionSize()
        self.deviceTableWidget.setShowGrid(False)
        self.deviceTableWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLabel, alignment=Qt.AlignHCenter)
        self.mainLayout.addWidget(self.deviceTableWidget)
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
        try:
            self.clearTableWidget()
            sceneName = info["SceneName"] if info["SceneName"] else ""
            if info["PlayName"]:
                self.titleLabel.setText("{}:({})".format(sceneName, info["PlayName"]))
            else:
                self.titleLabel.setText("")
            if not info["Device"]:
                return
            devices = info["Device"]
            self.deviceTableWidget.setRowCount(len(devices))
            row = 0
            for device in devices: # name pos speed uplimit downlimit
                devNameItem = QTableWidgetItem(device[0])
                devNameItem.setTextAlignment(Qt.AlignHCenter)
                self.deviceTableWidget.setItem(row, 0, devNameItem)
                posItem = QTableWidgetItem(str(device[1]))
                posItem.setTextAlignment(Qt.AlignHCenter)
                self.deviceTableWidget.setItem(row, 1, posItem)
                speedItem = QTableWidgetItem(str(device[2]))
                speedItem.setTextAlignment(Qt.AlignHCenter)
                self.deviceTableWidget.setItem(row, 2, speedItem)
                upRadioButton = QRadioButton()
                upRadioButton.setChecked(device[3])
                widget = QWidget()
                layout = QHBoxLayout()
                layout.addWidget(upRadioButton, alignment=Qt.AlignHCenter)
                layout.setContentsMargins(0,0,0,0)
                widget.setLayout(layout)
                self.deviceTableWidget.setCellWidget(row, 3, widget)
                downRadioButton = QRadioButton()
                downRadioButton.setChecked(device[4])
                widget = QWidget()
                layout = QHBoxLayout()
                layout.addWidget(downRadioButton, alignment=Qt.AlignHCenter)
                layout.setContentsMargins(0,0,0,0)
                widget.setLayout(layout)
                self.deviceTableWidget.setCellWidget(row, 4, widget)
                row += 1
        except Exception as e:
            print("show device error", str(e))
