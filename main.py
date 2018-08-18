#!/usr/bin/env python

import sys
from PyQt5.QtWidgets import *
from mainwindow import  *
from rcc import  rc_infoscreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    try:
        with open("infoscreen.qss", 'r') as qssFile:
            styleSheet = qssFile.readlines()
        qApp.setStyleSheet("".join(styleSheet))
    except Exception as e:
        print(str(e))
        QMessageBox.warning(None,
                            "Warning",
                            "Maybe you lost style sheet file for this Application",
                            QMessageBox.Ok)
    Config()
    w = MainWindow()
    sys.exit(app.exec_())


