# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainwindow(object):
    def setupUi(self, mainwindow):
        mainwindow.setObjectName("mainwindow")
        mainwindow.resize(669, 259)
        self.horizontalLayout = QtWidgets.QHBoxLayout(mainwindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame = QtWidgets.QFrame(mainwindow)
        self.frame.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frame.setFrameShape(QtWidgets.QFrame.Box)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.dateTimeLayout = QtWidgets.QVBoxLayout(self.frame)
        self.dateTimeLayout.setObjectName("dateTimeLayout")
        self.timeLabel = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeLabel.sizePolicy().hasHeightForWidth())
        self.timeLabel.setSizePolicy(sizePolicy)
        self.timeLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.dateTimeLayout.addWidget(self.timeLabel)
        self.weekLabel = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.weekLabel.sizePolicy().hasHeightForWidth())
        self.weekLabel.setSizePolicy(sizePolicy)
        self.weekLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.weekLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.weekLabel.setObjectName("weekLabel")
        self.dateTimeLayout.addWidget(self.weekLabel)
        self.dateLabel = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateLabel.sizePolicy().hasHeightForWidth())
        self.dateLabel.setSizePolicy(sizePolicy)
        self.dateLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.dateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.dateLabel.setObjectName("dateLabel")
        self.dateTimeLayout.addWidget(self.dateLabel)
        self.horizontalLayout.addWidget(self.frame)
        self.contentFrame = QtWidgets.QFrame(mainwindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.contentFrame.sizePolicy().hasHeightForWidth())
        self.contentFrame.setSizePolicy(sizePolicy)
        self.contentFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.contentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.contentFrame.setObjectName("contentFrame")
        self.horizontalLayout.addWidget(self.contentFrame)

        self.retranslateUi(mainwindow)
        QtCore.QMetaObject.connectSlotsByName(mainwindow)

    def retranslateUi(self, mainwindow):
        _translate = QtCore.QCoreApplication.translate
        mainwindow.setWindowTitle(_translate("mainwindow", "Form"))
        self.timeLabel.setText(_translate("mainwindow", "time"))
        self.weekLabel.setText(_translate("mainwindow", "week"))
        self.dateLabel.setText(_translate("mainwindow", "date"))

