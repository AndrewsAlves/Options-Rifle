# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'options_rifle_UI_2.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QFrame,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpinBox, QStatusBar, QTabWidget,
    QWidget)

class Ui_main(object):
    def setupUi(self, main):
        if not main.objectName():
            main.setObjectName(u"main")
        main.resize(357, 900)
        main.setMinimumSize(QSize(357, 900))
        main.setMaximumSize(QSize(357, 900))
        font = QFont()
        font.setFamilies([u"Graphie"])
        main.setFont(font)
        main.setAutoFillBackground(False)
        main.setStyleSheet(u"background:#27292F")
        main.setTabShape(QTabWidget.Rounded)
        self.MainWinodw2 = QWidget(main)
        self.MainWinodw2.setObjectName(u"MainWinodw2")
        self.MainWinodw2.setEnabled(True)
        self.MainWinodw2.setFocusPolicy(Qt.NoFocus)
        self.MainWinodw2.setAutoFillBackground(False)
        self.MainWinodw2.setStyleSheet(u"background: #27292F")
        self.btn_aggresive = QPushButton(self.MainWinodw2)
        self.btn_aggresive.setObjectName(u"btn_aggresive")
        self.btn_aggresive.setEnabled(True)
        self.btn_aggresive.setGeometry(QRect(230, 20, 91, 31))
        palette = QPalette()
        brush = QBrush(QColor(39, 41, 47, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        self.btn_aggresive.setPalette(palette)
        font1 = QFont()
        font1.setFamilies([u"Inter"])
        font1.setBold(False)
        self.btn_aggresive.setFont(font1)
        self.btn_aggresive.setAutoFillBackground(False)
        self.btn_aggresive.setStyleSheet(u"")
        self.btn_aggresive.setAutoDefault(False)
        self.btn_aggresive.setFlat(False)
        self.btn_defensive = QPushButton(self.MainWinodw2)
        self.btn_defensive.setObjectName(u"btn_defensive")
        self.btn_defensive.setGeometry(QRect(30, 20, 91, 31))
        font2 = QFont()
        font2.setFamilies([u"Inter"])
        self.btn_defensive.setFont(font2)
        self.btn_defensive.setAutoDefault(False)
        self.btn_defensive.setFlat(False)
        self.btn_bounce = QPushButton(self.MainWinodw2)
        self.btn_bounce.setObjectName(u"btn_bounce")
        self.btn_bounce.setEnabled(True)
        self.btn_bounce.setGeometry(QRect(130, 20, 91, 31))
        self.btn_bounce.setFont(font2)
        self.btn_bounce.setAutoDefault(False)
        self.btn_bounce.setFlat(False)
        self.spinner_ticker = QComboBox(self.MainWinodw2)
        self.spinner_ticker.setObjectName(u"spinner_ticker")
        self.spinner_ticker.setGeometry(QRect(30, 80, 161, 31))
        self.spinner_ticker.setFont(font2)
        self.spinner_ticker.setStyleSheet(u"color:#F3EF52;\n"
"")
        self.spinner_ticker.setMaxVisibleItems(10)
        self.spinner_ticker.setMaxCount(2147483646)
        self.btn_long = QPushButton(self.MainWinodw2)
        self.btn_long.setObjectName(u"btn_long")
        self.btn_long.setGeometry(QRect(250, 80, 31, 31))
        font3 = QFont()
        font3.setFamilies([u"Graphie"])
        font3.setBold(False)
        self.btn_long.setFont(font3)
        self.btn_long.setIconSize(QSize(28, 28))
        self.btn_short = QPushButton(self.MainWinodw2)
        self.btn_short.setObjectName(u"btn_short")
        self.btn_short.setGeometry(QRect(290, 80, 31, 31))
        self.btn_short.setFont(font)
        self.btn_short.setIconSize(QSize(28, 28))
        self.line = QFrame(self.MainWinodw2)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(30, 60, 291, 16))
        self.line.setStyleSheet(u"color:#3B3D44")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.label_riskpertrade = QLabel(self.MainWinodw2)
        self.label_riskpertrade.setObjectName(u"label_riskpertrade")
        self.label_riskpertrade.setGeometry(QRect(30, 811, 80, 16))
        self.label_riskpertrade.setFont(font2)
        self.label_riskpertrade.setStyleSheet(u"color:white")
        self.et_risk = QLineEdit(self.MainWinodw2)
        self.et_risk.setObjectName(u"et_risk")
        self.et_risk.setEnabled(True)
        self.et_risk.setGeometry(QRect(30, 833, 91, 21))
        self.et_risk.setFont(font2)
        self.et_risk.setStyleSheet(u"QLineEdit {\n"
"        background-color: #0000000;\n"
"        border: 1px solid white;\n"
"		color:white;\n"
"		border-radius:5px\n"
"    }")
        self.label_mtm_label = QLabel(self.MainWinodw2)
        self.label_mtm_label.setObjectName(u"label_mtm_label")
        self.label_mtm_label.setGeometry(QRect(280, 742, 41, 21))
        font4 = QFont()
        font4.setFamilies([u"Inter"])
        font4.setPointSize(12)
        self.label_mtm_label.setFont(font4)
        self.label_mtm_label.setStyleSheet(u"color:#9F9F9F")
        self.label_MTM = QLabel(self.MainWinodw2)
        self.label_MTM.setObjectName(u"label_MTM")
        self.label_MTM.setGeometry(QRect(80, 768, 241, 31))
        font5 = QFont()
        font5.setFamilies([u"Inter"])
        font5.setPointSize(24)
        self.label_MTM.setFont(font5)
        self.label_MTM.setStyleSheet(u"color:white")
        self.label_MTM.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.btn_execute = QPushButton(self.MainWinodw2)
        self.btn_execute.setObjectName(u"btn_execute")
        self.btn_execute.setGeometry(QRect(230, 827, 91, 31))
        palette1 = QPalette()
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        brush2 = QBrush(QColor(243, 239, 82, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette1.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush1)
        palette1.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette1.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette1.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.btn_execute.setPalette(palette1)
        font6 = QFont()
        self.btn_execute.setFont(font6)
        self.btn_execute.setStyleSheet(u"QPushButton  {\n"
"  font-size:12px;\n"
"  width:140px;\n"
"  height:50px;\n"
"  border-width:1px;\n"
"  color:rgba(0, 0, 0, 1);\n"
"  border-color:rgba(24, 171, 41, 0);\n"
"  border-radius:15px;\n"
"  background:rgba(243, 239, 82, 1);\n"
"}\n"
"\n"
"QPushButton :hover {\n"
"  background: rgba(191, 188, 50, 1)!important;\n"
"}")
        self.btn_execute.setAutoDefault(False)
        self.btn_execute.setFlat(False)
        self.line_2 = QFrame(self.MainWinodw2)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(29, 723, 291, 16))
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.label_label_spot = QLabel(self.MainWinodw2)
        self.label_label_spot.setObjectName(u"label_label_spot")
        self.label_label_spot.setGeometry(QRect(30, 130, 47, 13))
        self.label_label_spot.setFont(font2)
        self.label_label_spot.setStyleSheet(u"color:#9F9F9F")
        self.label_spot = QLabel(self.MainWinodw2)
        self.label_spot.setObjectName(u"label_spot")
        self.label_spot.setGeometry(QRect(30, 150, 81, 16))
        font7 = QFont()
        font7.setFamilies([u"Inter"])
        font7.setPointSize(11)
        font7.setBold(False)
        self.label_spot.setFont(font7)
        self.label_spot.setStyleSheet(u"color:white")
        self.label_futures = QLabel(self.MainWinodw2)
        self.label_futures.setObjectName(u"label_futures")
        self.label_futures.setGeometry(QRect(150, 150, 81, 16))
        self.label_futures.setFont(font7)
        self.label_futures.setStyleSheet(u"color:white")
        self.label_label_futures = QLabel(self.MainWinodw2)
        self.label_label_futures.setObjectName(u"label_label_futures")
        self.label_label_futures.setGeometry(QRect(150, 130, 47, 13))
        self.label_label_futures.setFont(font2)
        self.label_label_futures.setStyleSheet(u"color:#9F9F9F")
        self.label_future_diff = QLabel(self.MainWinodw2)
        self.label_future_diff.setObjectName(u"label_future_diff")
        self.label_future_diff.setGeometry(QRect(250, 150, 71, 20))
        font8 = QFont()
        font8.setFamilies([u"Inter"])
        font8.setPointSize(11)
        self.label_future_diff.setFont(font8)
        self.label_future_diff.setStyleSheet(u"color:white")
        self.label_label_futures_diff = QLabel(self.MainWinodw2)
        self.label_label_futures_diff.setObjectName(u"label_label_futures_diff")
        self.label_label_futures_diff.setGeometry(QRect(250, 130, 71, 16))
        self.label_label_futures_diff.setFont(font2)
        self.label_label_futures_diff.setStyleSheet(u"color:#9F9F9F")
        self.line_3 = QFrame(self.MainWinodw2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(30, 490, 291, 16))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.spin_stoploss = QSpinBox(self.MainWinodw2)
        self.spin_stoploss.setObjectName(u"spin_stoploss")
        self.spin_stoploss.setGeometry(QRect(110, 210, 131, 31))
        palette2 = QPalette()
        brush3 = QBrush(QColor(255, 255, 255, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.WindowText, brush3)
        palette2.setBrush(QPalette.Active, QPalette.Button, brush)
        palette2.setBrush(QPalette.Active, QPalette.Text, brush3)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush3)
        palette2.setBrush(QPalette.Active, QPalette.Base, brush)
        palette2.setBrush(QPalette.Active, QPalette.Window, brush)
        palette2.setBrush(QPalette.Active, QPalette.Highlight, brush2)
        palette2.setBrush(QPalette.Active, QPalette.HighlightedText, brush1)
        palette2.setBrush(QPalette.Active, QPalette.Link, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.WindowText, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Text, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Window, brush)
        palette2.setBrush(QPalette.Inactive, QPalette.Highlight, brush2)
        palette2.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush1)
        palette2.setBrush(QPalette.Inactive, QPalette.Link, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.WindowText, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Text, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        palette2.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette2.setBrush(QPalette.Disabled, QPalette.Window, brush)
        brush4 = QBrush(QColor(0, 120, 215, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Disabled, QPalette.Highlight, brush4)
        palette2.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush1)
        palette2.setBrush(QPalette.Disabled, QPalette.Link, brush2)
        self.spin_stoploss.setPalette(palette2)
        self.spin_stoploss.setFont(font4)
        self.spin_stoploss.setStyleSheet(u"color:white;")
        self.spin_stoploss.setAlignment(Qt.AlignCenter)
        self.spin_stoploss.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_stoploss.setMaximum(1000000)
        self.label_stoploss = QLabel(self.MainWinodw2)
        self.label_stoploss.setObjectName(u"label_stoploss")
        self.label_stoploss.setGeometry(QRect(151, 250, 51, 16))
        self.label_stoploss.setFont(font2)
        self.label_stoploss.setStyleSheet(u"color:white")
        self.btn_editrisk = QPushButton(self.MainWinodw2)
        self.btn_editrisk.setObjectName(u"btn_editrisk")
        self.btn_editrisk.setGeometry(QRect(126, 833, 21, 21))
        self.btn_editrisk.setFont(font3)
        self.btn_editrisk.setStyleSheet(u"background:#00000000")
        icon = QIcon()
        icon.addFile(u"../../icons/btn_edit_risk.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_editrisk.setIcon(icon)
        self.btn_editrisk.setIconSize(QSize(20, 20))
        self.btn_trans_label_Fut = QPushButton(self.MainWinodw2)
        self.btn_trans_label_Fut.setObjectName(u"btn_trans_label_Fut")
        self.btn_trans_label_Fut.setGeometry(QRect(150, 150, 75, 23))
        self.btn_trans_label_Fut.setStyleSheet(u"background-color: transparent; border: none;")
        self.frame_trade = QFrame(self.MainWinodw2)
        self.frame_trade.setObjectName(u"frame_trade")
        self.frame_trade.setGeometry(QRect(30, 511, 291, 208))
        self.frame_trade.setFrameShape(QFrame.NoFrame)
        self.frame_trade.setFrameShadow(QFrame.Plain)
        self.icon_trade_type = QPushButton(self.frame_trade)
        self.icon_trade_type.setObjectName(u"icon_trade_type")
        self.icon_trade_type.setGeometry(QRect(4, 5, 31, 31))
        self.icon_trade_type.setStyleSheet(u"background:rgba(0, 0, 0, 0);")
        icon1 = QIcon()
        icon1.addFile(u"../../icons/icon_arrow_long.png", QSize(), QIcon.Normal, QIcon.Off)
        self.icon_trade_type.setIcon(icon1)
        self.icon_trade_type.setIconSize(QSize(26, 26))
        self.label_instrument = QLabel(self.frame_trade)
        self.label_instrument.setObjectName(u"label_instrument")
        self.label_instrument.setGeometry(QRect(105, 11, 177, 16))
        font9 = QFont()
        font9.setFamilies([u"Inter"])
        font9.setPointSize(14)
        font9.setBold(True)
        self.label_instrument.setFont(font9)
        self.label_instrument.setStyleSheet(u"color:white")
        self.label_instrument.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.border_label = QLabel(self.frame_trade)
        self.border_label.setObjectName(u"border_label")
        self.border_label.setGeometry(QRect(0, 0, 291, 208))
        self.border_label.setStyleSheet(u"border-radius: 9px; \n"
"border:1px solid #FFFFFF;")
        self.label_label_qty = QLabel(self.frame_trade)
        self.label_label_qty.setObjectName(u"label_label_qty")
        self.label_label_qty.setGeometry(QRect(53, 46, 21, 16))
        self.label_label_qty.setFont(font2)
        self.label_label_qty.setStyleSheet(u"color:#9F9F9F")
        self.label_label_avg = QLabel(self.frame_trade)
        self.label_label_avg.setObjectName(u"label_label_avg")
        self.label_label_avg.setGeometry(QRect(134, 46, 21, 16))
        self.label_label_avg.setFont(font2)
        self.label_label_avg.setStyleSheet(u"color:#9F9F9F")
        self.label_3 = QLabel(self.frame_trade)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(216, 46, 21, 16))
        self.label_3.setFont(font2)
        self.label_3.setStyleSheet(u"color:#9F9F9F")
        self.label_trade_qty = QLabel(self.frame_trade)
        self.label_trade_qty.setObjectName(u"label_trade_qty")
        self.label_trade_qty.setGeometry(QRect(31, 66, 61, 16))
        self.label_trade_qty.setFont(font7)
        self.label_trade_qty.setStyleSheet(u"color:white")
        self.label_trade_qty.setAlignment(Qt.AlignCenter)
        self.label_avg_price = QLabel(self.frame_trade)
        self.label_avg_price.setObjectName(u"label_avg_price")
        self.label_avg_price.setGeometry(QRect(114, 66, 61, 16))
        self.label_avg_price.setFont(font7)
        self.label_avg_price.setStyleSheet(u"color:white")
        self.label_avg_price.setAlignment(Qt.AlignCenter)
        self.label_trade_ltp = QLabel(self.frame_trade)
        self.label_trade_ltp.setObjectName(u"label_trade_ltp")
        self.label_trade_ltp.setGeometry(QRect(196, 66, 61, 16))
        self.label_trade_ltp.setFont(font7)
        self.label_trade_ltp.setStyleSheet(u"color:white")
        self.label_trade_ltp.setAlignment(Qt.AlignCenter)
        self.label_strategy = QLabel(self.frame_trade)
        self.label_strategy.setObjectName(u"label_strategy")
        self.label_strategy.setGeometry(QRect(31, 4, 31, 31))
        font10 = QFont()
        font10.setFamilies([u"Inter"])
        font10.setPointSize(9)
        font10.setBold(True)
        self.label_strategy.setFont(font10)
        self.label_strategy.setStyleSheet(u"background:rgba(0, 0, 0, 0);color:white")
        self.label_strategy.setAlignment(Qt.AlignCenter)
        self.label = QLabel(self.frame_trade)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(140, 94, 16, 21))
        font11 = QFont()
        font11.setFamilies([u"Inter"])
        font11.setPointSize(10)
        font11.setBold(False)
        self.label.setFont(font11)
        self.label.setStyleSheet(u"color:#9F9F9F")
        self.label_profit = QLabel(self.frame_trade)
        self.label_profit.setObjectName(u"label_profit")
        self.label_profit.setGeometry(QRect(148, 173, 131, 31))
        self.label_profit.setFont(font4)
        self.label_profit.setStyleSheet(u"color:white")
        self.label_profit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_risk = QLabel(self.frame_trade)
        self.label_risk.setObjectName(u"label_risk")
        self.label_risk.setGeometry(QRect(9, 173, 131, 31))
        self.label_risk.setFont(font4)
        self.label_risk.setStyleSheet(u"color:white")
        self.label_risk.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.label_label_risk = QLabel(self.frame_trade)
        self.label_label_risk.setObjectName(u"label_label_risk")
        self.label_label_risk.setGeometry(QRect(10, 164, 47, 13))
        self.label_label_risk.setFont(font2)
        self.label_label_risk.setStyleSheet(u"color:#9F9F9F")
        self.label_label_profit = QLabel(self.frame_trade)
        self.label_label_profit.setObjectName(u"label_label_profit")
        self.label_label_profit.setGeometry(QRect(229, 164, 47, 13))
        self.label_label_profit.setFont(font2)
        self.label_label_profit.setStyleSheet(u"color:#9F9F9F")
        self.label_label_profit.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.frame = QFrame(self.frame_trade)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(90, 120, 113, 60))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.border_label_2 = QLabel(self.frame)
        self.border_label_2.setObjectName(u"border_label_2")
        self.border_label_2.setGeometry(QRect(0, 0, 113, 32))
        self.border_label_2.setStyleSheet(u"border-radius: 9px; \n"
"border:1px solid #FFFFFF;")
        self.et_stoploss = QLineEdit(self.frame)
        self.et_stoploss.setObjectName(u"et_stoploss")
        self.et_stoploss.setGeometry(QRect(26, 1, 61, 27))
        self.et_stoploss.setFont(font8)
        self.et_stoploss.setStyleSheet(u"QLineEdit {\n"
"        background-color: #0000000;\n"
"        border: 1px solid #0000000;\n"
"		color:white;\n"
"		border-radius:5px;\n"
"    }")
        self.et_stoploss.setAlignment(Qt.AlignCenter)
        self.btn_increase_sl = QPushButton(self.frame)
        self.btn_increase_sl.setObjectName(u"btn_increase_sl")
        self.btn_increase_sl.setGeometry(QRect(89, 2, 21, 29))
        self.btn_increase_sl.setStyleSheet(u"background:rgba(0, 0, 0, 0);")
        icon2 = QIcon()
        icon2.addFile(u"../../icons/btn_plus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_increase_sl.setIcon(icon2)
        self.btn_increase_sl.setIconSize(QSize(18, 18))
        self.btn_decrease_sl = QPushButton(self.frame)
        self.btn_decrease_sl.setObjectName(u"btn_decrease_sl")
        self.btn_decrease_sl.setGeometry(QRect(4, 1, 21, 30))
        self.btn_decrease_sl.setStyleSheet(u"background:rgba(0, 0, 0, 0);")
        icon3 = QIcon()
        icon3.addFile(u"../../icons/btn_minus.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_decrease_sl.setIcon(icon3)
        self.btn_decrease_sl.setIconSize(QSize(18, 18))
        self.btn_edit_sl = QPushButton(self.frame)
        self.btn_edit_sl.setObjectName(u"btn_edit_sl")
        self.btn_edit_sl.setGeometry(QRect(45, 36, 23, 23))
        self.btn_edit_sl.setStyleSheet(u"background:rgba(0, 0, 0, 0);")
        icon4 = QIcon()
        icon4.addFile(u"../../icons/btn_edit_sl.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_edit_sl.setIcon(icon4)
        self.btn_edit_sl.setIconSize(QSize(18, 18))
        self.border_label_2.raise_()
        self.btn_increase_sl.raise_()
        self.btn_decrease_sl.raise_()
        self.btn_edit_sl.raise_()
        self.et_stoploss.raise_()
        self.border_label.raise_()
        self.icon_trade_type.raise_()
        self.label_instrument.raise_()
        self.label_label_qty.raise_()
        self.label_label_avg.raise_()
        self.label_3.raise_()
        self.label_trade_qty.raise_()
        self.label_avg_price.raise_()
        self.label_trade_ltp.raise_()
        self.label_strategy.raise_()
        self.label.raise_()
        self.label_profit.raise_()
        self.label_risk.raise_()
        self.label_label_risk.raise_()
        self.label_label_profit.raise_()
        self.frame.raise_()
        self.label_no_position = QLabel(self.MainWinodw2)
        self.label_no_position.setObjectName(u"label_no_position")
        self.label_no_position.setGeometry(QRect(104, 602, 154, 15))
        self.label_no_position.setFont(font2)
        self.label_no_position.setStyleSheet(u"color:#6B6B6B;")
        self.label_no_position.setAlignment(Qt.AlignCenter)
        self.btn_exit = QPushButton(self.MainWinodw2)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(230, 827, 91, 31))
        palette3 = QPalette()
        palette3.setBrush(QPalette.Active, QPalette.WindowText, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Button, brush2)
        palette3.setBrush(QPalette.Active, QPalette.Text, brush1)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush1)
        palette3.setBrush(QPalette.Active, QPalette.Base, brush2)
        palette3.setBrush(QPalette.Active, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Inactive, QPalette.WindowText, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Button, brush2)
        palette3.setBrush(QPalette.Inactive, QPalette.Text, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush1)
        palette3.setBrush(QPalette.Inactive, QPalette.Base, brush2)
        palette3.setBrush(QPalette.Inactive, QPalette.Window, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Button, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Text, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        palette3.setBrush(QPalette.Disabled, QPalette.Base, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.Window, brush2)
        self.btn_exit.setPalette(palette3)
        self.btn_exit.setFont(font6)
        self.btn_exit.setStyleSheet(u"QPushButton  {\n"
"  font-size:12px;\n"
"  width:140px;\n"
"  height:50px;\n"
"  border-width:1px;\n"
"  color:rgba(0, 0, 0, 1);\n"
"  border-color:rgba(24, 171, 41, 0);\n"
"  border-radius:15px;\n"
"  background:rgba(243, 239, 82, 1);\n"
"}\n"
"\n"
"QPushButton :hover {\n"
"  background: rgba(191, 188, 50, 1)!important;\n"
"}")
        self.btn_exit.setAutoDefault(False)
        self.btn_exit.setFlat(False)
        main.setCentralWidget(self.MainWinodw2)
        self.btn_exit.raise_()
        self.btn_long.raise_()
        self.btn_aggresive.raise_()
        self.btn_defensive.raise_()
        self.btn_bounce.raise_()
        self.spinner_ticker.raise_()
        self.btn_short.raise_()
        self.line.raise_()
        self.label_riskpertrade.raise_()
        self.et_risk.raise_()
        self.label_mtm_label.raise_()
        self.label_MTM.raise_()
        self.btn_execute.raise_()
        self.line_2.raise_()
        self.label_label_spot.raise_()
        self.label_spot.raise_()
        self.label_futures.raise_()
        self.label_label_futures.raise_()
        self.label_future_diff.raise_()
        self.label_label_futures_diff.raise_()
        self.line_3.raise_()
        self.spin_stoploss.raise_()
        self.label_stoploss.raise_()
        self.btn_editrisk.raise_()
        self.btn_trans_label_Fut.raise_()
        self.frame_trade.raise_()
        self.label_no_position.raise_()
        self.statusbar = QStatusBar(main)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setStyleSheet(u"color:#F3EF52;")
        main.setStatusBar(self.statusbar)

        self.retranslateUi(main)

        self.btn_aggresive.setDefault(False)
        self.btn_defensive.setDefault(False)
        self.btn_bounce.setDefault(False)
        self.btn_execute.setDefault(False)
        self.btn_exit.setDefault(False)


        QMetaObject.connectSlotsByName(main)
    # setupUi

    def retranslateUi(self, main):
        main.setWindowTitle(QCoreApplication.translate("main", u"Options Rifle", None))
        self.btn_aggresive.setText(QCoreApplication.translate("main", u"Aggresive", None))
        self.btn_defensive.setText(QCoreApplication.translate("main", u"Defensive", None))
        self.btn_bounce.setText(QCoreApplication.translate("main", u"Bounce", None))
        self.btn_long.setText("")
        self.btn_short.setText("")
        self.label_riskpertrade.setText(QCoreApplication.translate("main", u"Risk Per Trade", None))
        self.label_mtm_label.setText(QCoreApplication.translate("main", u"MTM", None))
        self.label_MTM.setText(QCoreApplication.translate("main", u"0.0", None))
        self.btn_execute.setText(QCoreApplication.translate("main", u"Execute", None))
        self.label_label_spot.setText(QCoreApplication.translate("main", u"Spot", None))
        self.label_spot.setText(QCoreApplication.translate("main", u"0.0", None))
        self.label_futures.setText(QCoreApplication.translate("main", u"0.0", None))
        self.label_label_futures.setText(QCoreApplication.translate("main", u"Futures", None))
        self.label_future_diff.setText(QCoreApplication.translate("main", u"0.0", None))
        self.label_label_futures_diff.setText(QCoreApplication.translate("main", u"Premium DIff.", None))
        self.label_stoploss.setText(QCoreApplication.translate("main", u"Stop loss", None))
        self.btn_editrisk.setText("")
        self.btn_trans_label_Fut.setText("")
        self.icon_trade_type.setText("")
        self.label_instrument.setText(QCoreApplication.translate("main", u"45000 CE", None))
        self.border_label.setText("")
        self.label_label_qty.setText(QCoreApplication.translate("main", u"Qty", None))
        self.label_label_avg.setText(QCoreApplication.translate("main", u"Avg.", None))
        self.label_3.setText(QCoreApplication.translate("main", u"LTP", None))
        self.label_trade_qty.setText(QCoreApplication.translate("main", u"0", None))
        self.label_avg_price.setText(QCoreApplication.translate("main", u"0.0", None))
        self.label_trade_ltp.setText(QCoreApplication.translate("main", u"0.0", None))
        self.label_strategy.setText(QCoreApplication.translate("main", u"AT", None))
        self.label.setText(QCoreApplication.translate("main", u"SL", None))
        self.label_profit.setText(QCoreApplication.translate("main", u"+10,900", None))
        self.label_risk.setText(QCoreApplication.translate("main", u"10,900", None))
        self.label_label_risk.setText(QCoreApplication.translate("main", u"Risk", None))
        self.label_label_profit.setText(QCoreApplication.translate("main", u"Profit", None))
        self.border_label_2.setText("")
        self.et_stoploss.setText(QCoreApplication.translate("main", u"223", None))
        self.btn_increase_sl.setText("")
        self.btn_decrease_sl.setText("")
        self.btn_edit_sl.setText("")
        self.label_no_position.setText(QCoreApplication.translate("main", u"You dont have any position", None))
        self.btn_exit.setText(QCoreApplication.translate("main", u"Exit", None))
    # retranslateUi

