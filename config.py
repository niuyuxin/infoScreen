#!/usr/bin/env python
# -*- coding:utf8 -*-

from PyQt5.QtCore import *
import re
class Config(object):
    version = "18.07.08.3"
    SettingsName = "infoScreen.ini"
    serverIp = "ServerIp"
    monitorName = "MonitorName"
    monitorId = "MonitorId"
    SectionSize = "SectionSize"
    def __init__(self):
        set = QSettings(Config.SettingsName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"));
        if Config.version != str(set.value("Version")):
            set.clear()
            set.setValue("Version", Config.version)
            set.setValue(Config.monitorName, "infoScreen")
            set.setValue(Config.serverIp, "127.0.0.1")
            set.setValue(Config.monitorId, 0)
            set.setValue(Config.SectionSize, 1)
            set.sync()
    @staticmethod
    def value(key):
        set = QSettings(Config.SettingsName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"))
        return set.value(key)
    @staticmethod
    def setValue(key, value):
        set = QSettings(Config.SettingsName, QSettings.IniFormat)
        set.setIniCodec(QTextCodec.codecForName("UTF-8"))
        return set.setValue(key, value)

