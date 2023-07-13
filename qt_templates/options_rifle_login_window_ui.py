# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options_rifle_login_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(405, 244)
        MainWindow.setStyleSheet(u"background:#27292F")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(130, 50, 141, 21))
        font = QFont()
        font.setFamilies([u"Graphie"])
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:#F3EF52;")
        self.btn_login = QPushButton(self.centralwidget)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setGeometry(QRect(62, 110, 131, 41))
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        self.btn_login.setFont(font1)
        self.btn_login.setStyleSheet(u"background:#F3EF52;")
        self.label_process = QLabel(self.centralwidget)
        self.label_process.setObjectName(u"label_process")
        self.label_process.setGeometry(QRect(40, 180, 321, 20))
        self.label_process.setStyleSheet(u"color:white")
        self.label_process.setAlignment(Qt.AlignCenter)
        self.btn_login_angel = QPushButton(self.centralwidget)
        self.btn_login_angel.setObjectName(u"btn_login_angel")
        self.btn_login_angel.setGeometry(QRect(211, 110, 131, 41))
        self.btn_login_angel.setFont(font1)
        self.btn_login_angel.setStyleSheet(u"background:#F3EF52;")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Login", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Options Rifle", None))
        self.btn_login.setText(QCoreApplication.translate("MainWindow", u"Login To Zerodha", None))
        self.label_process.setText("")
        self.btn_login_angel.setText(QCoreApplication.translate("MainWindow", u"Login To Angel One", None))
    # retranslateUi

