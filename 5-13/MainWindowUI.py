# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'S:\Python\sapper\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(560, 538)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 541, 501))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.timeLcdNumber = QtWidgets.QLCDNumber(self.verticalLayoutWidget_2)
        # self.timeLcdNumber.setMinimumSize(QtCore.QSize(0, 40))
        # self.timeLcdNumber.setMaximumSize(QtCore.QSize(197, 16777215))
        # self.timeLcdNumber.setObjectName("timeLcdNumber")
        # self.horizontalLayout.addWidget(self.timeLcdNumber, 0, QtCore.Qt.AlignLeft)
        # self.scoreNum = QLabel(self.verticalLayoutWidget_2)
        # self.scoreNum.setMinimumSize(QtCore.QSize(0, 40))
        # self.scoreNum.setMaximumSize(QtCore.QSize(197, 16777215))
        # self.scoreNum.setObjectName("scoreNum")
        # self.horizontalLayout.addWidget(self.timeLcdNumber, 0, QtCore.Qt.AlignLeft)
        self.confirmChainPushButton = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.confirmChainPushButton.setObjectName("newGamePushButton")
        self.horizontalLayout.addWidget(self.confirmChainPushButton, 0, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gameFieldTableView = QtWidgets.QTableView(self.verticalLayoutWidget_2)
        self.gameFieldTableView.setStyleSheet("QTableView { gridline-color: green; }")
        self.gameFieldTableView.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.gameFieldTableView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.gameFieldTableView.setObjectName("gameFieldTableView")
        self.gameFieldTableView.horizontalHeader().setVisible(False)
        self.gameFieldTableView.horizontalHeader().setDefaultSectionSize(30)
        self.gameFieldTableView.verticalHeader().setVisible(False)
        self.verticalLayout_2.addWidget(self.gameFieldTableView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 560, 18))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName("action")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_5 = QtWidgets.QAction(MainWindow)
        self.action_5.setObjectName("action_5")
        self.menu.addAction(self.action)
        self.menu.addAction(self.action_2)
        self.menu.addSeparator()
        self.menu.addAction(self.action_5)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.confirmChainPushButton.setText(_translate("MainWindow", "Подтвердить цепочку"))
        self.menu.setTitle(_translate("MainWindow", "Игра"))
        self.action.setText(_translate("MainWindow", "&Новая"))
        self.action_2.setText(_translate("MainWindow", "&Параметры"))
        self.action_3.setText(_translate("MainWindow", "-"))
        self.action_5.setText(_translate("MainWindow", "&Выход"))

