# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mask_window.ui'
##
## Created by: Qt User Interface Compiler version 6.0.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1103, 551)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(150, 430, 801, 51))
        self.progressBar.setValue(0)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(430, 10, 201, 51))
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setUnderline(True)
        self.label.setFont(font)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(210, 120, 481, 51))
        font1 = QFont()
        font1.setPointSize(14)
        self.label_2.setFont(font1)
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(210, 180, 161, 21))
        self.label_3.setFont(font1)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(210, 220, 651, 41))
        self.label_4.setFont(font1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1103, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0418\u043d\u0441\u0442\u0440\u0443\u043a\u0446\u0438\u044f", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"1. \u041f\u0435\u0440\u0435\u0434 \u0438\u0441\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u043d\u0438\u0435\u043c \u043c\u0430\u0441\u043a\u0438 \u043d\u0430\u0441\u0443\u0445\u043e \u0432\u044b\u0442\u0440\u0435\u0442\u0435 \u043b\u0438\u0446\u043e.", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"2. \u041d\u0430\u0434\u0435\u043d\u044c\u0442\u0435 \u043c\u0430\u0441\u043a\u0443.", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"3. \u041d\u0435 \u0441\u043d\u0438\u043c\u0430\u0439\u0442\u0435 \u043c\u0430\u0441\u043a\u0443, \u043f\u043e\u043a\u0430 \u043e\u043d\u0430 \u0440\u0430\u0431\u043e\u0442\u0430\u0435\u0442. \u041d\u0435 \u0434\u0435\u043b\u0430\u0439\u0442\u0435 \u0440\u0435\u0437\u043a\u0438\u0445 \u0434\u0432\u0438\u0436\u0435\u043d\u0438\u0439.", None))
    # retranslateUi

