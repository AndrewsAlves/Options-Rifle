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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(405, 244)
        MainWindow.setStyleSheet(u"background:#27292F")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.frame_main = QFrame(self.centralwidget)
        self.frame_main.setObjectName(u"frame_main")
        self.frame_main.setGeometry(QRect(10, 10, 405, 211))
        self.frame_main.setFrameShape(QFrame.StyledPanel)
        self.frame_main.setFrameShadow(QFrame.Raised)
        self.label = QLabel(self.frame_main)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(119, 30, 141, 21))
        font = QFont()
        font.setFamilies([u"Graphie"])
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color:#F3EF52;")
        self.btn_login = QPushButton(self.frame_main)
        self.btn_login.setObjectName(u"btn_login")
        self.btn_login.setGeometry(QRect(51, 90, 131, 41))
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        self.btn_login.setFont(font1)
        self.btn_login.setStyleSheet(u"background:#F3EF52;")
        self.btn_login_angel = QPushButton(self.frame_main)
        self.btn_login_angel.setObjectName(u"btn_login_angel")
        self.btn_login_angel.setGeometry(QRect(200, 90, 131, 41))
        self.btn_login_angel.setFont(font1)
        self.btn_login_angel.setStyleSheet(u"background:#F3EF52;")
        self.frame_login_zerodha_api = QFrame(self.centralwidget)
        self.frame_login_zerodha_api.setObjectName(u"frame_login_zerodha_api")
        self.frame_login_zerodha_api.setGeometry(QRect(10, 10, 405, 211))
        self.frame_login_zerodha_api.setFrameShape(QFrame.StyledPanel)
        self.frame_login_zerodha_api.setFrameShadow(QFrame.Raised)
        self.label_process = QLabel(self.frame_login_zerodha_api)
        self.label_process.setObjectName(u"label_process")
        self.label_process.setGeometry(QRect(29, 179, 321, 20))
        self.label_process.setStyleSheet(u"color:white")
        self.label_process.setAlignment(Qt.AlignCenter)
        self.btn_login_zerodha_api = QPushButton(self.frame_login_zerodha_api)
        self.btn_login_zerodha_api.setObjectName(u"btn_login_zerodha_api")
        self.btn_login_zerodha_api.setGeometry(QRect(126, 125, 131, 41))
        self.btn_login_zerodha_api.setFont(font1)
        self.btn_login_zerodha_api.setStyleSheet(u"background:#F3EF52;")
        self.lineedit_apikey = QLineEdit(self.frame_login_zerodha_api)
        self.lineedit_apikey.setObjectName(u"lineedit_apikey")
        self.lineedit_apikey.setGeometry(QRect(32, 40, 321, 20))
        self.lineedit_apikey.setStyleSheet(u"color:white;")
        self.label_3 = QLabel(self.frame_login_zerodha_api)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(34, 23, 47, 13))
        self.label_3.setStyleSheet(u"color:gray;")
        self.label_4 = QLabel(self.frame_login_zerodha_api)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(32, 64, 61, 16))
        self.label_4.setStyleSheet(u"color:gray;")
        self.lineedit_api_secret = QLineEdit(self.frame_login_zerodha_api)
        self.lineedit_api_secret.setObjectName(u"lineedit_api_secret")
        self.lineedit_api_secret.setGeometry(QRect(32, 83, 321, 20))
        self.lineedit_api_secret.setStyleSheet(u"color:white;")
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
        self.btn_login_angel.setText(QCoreApplication.translate("MainWindow", u"Login To Angel One", None))
        self.label_process.setText("")
        self.btn_login_zerodha_api.setText(QCoreApplication.translate("MainWindow", u"Login To Zerodha", None))
        self.lineedit_apikey.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"API key", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"API secret", None))
    # retranslateUi

