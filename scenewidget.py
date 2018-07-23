#!/usr/bin/env python3

from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *

class SceneWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLable = QLabel("标题")
        self.progressBar = QProgressBar()
        self.deviceTableWidget = QTableWidget()
        self.deviceTableWidget.setColumnCount(5)
        hHeaderLabels = ["设备名称", "位置", "速度", "上限", "下限"]
        self.deviceTableWidget.setHorizontalHeaderLabels(hHeaderLabels)
        self.deviceTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.deviceTableWidget.verticalHeader().setHidden(True)
        self.deviceTableWidget.setShowGrid(False)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.titleLable, alignment=Qt.AlignHCenter)
        self.mainLayout.addWidget(self.progressBar)
        self.mainLayout.addWidget(self.deviceTableWidget)
        self.setLayout(self.mainLayout)
    def showDevice(self, info): # name, pos, speed, uplimit, downlimit
        try:
            self.deviceTableWidget.clear()
            hHeaderLabels = ["设备名称", "位置", "速度", "上限", "下限"]
            self.deviceTableWidget.setHorizontalHeaderLabels(hHeaderLabels)
            self.deviceTableWidget.setRowCount(5)
            for i in range(5):
                upRadioButton = QRadioButton()
                downRadioButton = QRadioButton()
                widget = QWidget()
                layout = QHBoxLayout()
                layout.addWidget(upRadioButton, alignment=Qt.AlignHCenter)
                layout.setContentsMargins(0,0,0,0)
                widget.setLayout(layout)
                self.deviceTableWidget.setCellWidget(i, 3, widget)
                widget = QWidget()
                layout = QHBoxLayout()
                layout.addWidget(downRadioButton, alignment=Qt.AlignHCenter)
                layout.setContentsMargins(0,0,0,0)
                widget.setLayout(layout)
                self.deviceTableWidget.setCellWidget(i, 4, widget)
                for c in range(3):
                    tableWidgetItem = QTableWidgetItem()
                    tableWidgetItem.setText("None")
                    self.deviceTableWidget.setItem(i, c, tableWidgetItem)
        except Exception as e:
            print(str(e))
