# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'steel_inp22222.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(369, 118)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 341, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 4, 1, 1)
        self.sig_in_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.sig_in_2.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.sig_in_2.setObjectName("sig_in_2")
        self.gridLayout.addWidget(self.sig_in_2, 1, 0, 1, 1)
        self.sig_in = QtWidgets.QLineEdit(self.layoutWidget)
        self.sig_in.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.sig_in.setObjectName("sig_in")
        self.gridLayout.addWidget(self.sig_in, 1, 1, 1, 1)
        self.a_in = QtWidgets.QLineEdit(self.layoutWidget)
        self.a_in.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.a_in.setObjectName("a_in")
        self.gridLayout.addWidget(self.a_in, 1, 2, 1, 1)
        self.b_in = QtWidgets.QLineEdit(self.layoutWidget)
        self.b_in.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.b_in.setObjectName("b_in")
        self.gridLayout.addWidget(self.b_in, 1, 3, 1, 1)
        self.c_in = QtWidgets.QLineEdit(self.layoutWidget)
        self.c_in.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.c_in.setObjectName("c_in")
        self.gridLayout.addWidget(self.c_in, 1, 4, 1, 1)
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(100, 80, 158, 25))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.bt_OK = QtWidgets.QPushButton(self.widget)
        self.bt_OK.setObjectName("bt_OK")
        self.gridLayout_2.addWidget(self.bt_OK, 0, 0, 1, 1)
        self.bt_STOP = QtWidgets.QPushButton(self.widget)
        self.bt_STOP.setObjectName("bt_STOP")
        self.gridLayout_2.addWidget(self.bt_STOP, 0, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "Название"))
        self.label.setText(_translate("Dialog", "сигма"))
        self.label_2.setText(_translate("Dialog", "a"))
        self.label_3.setText(_translate("Dialog", "b"))
        self.label_4.setText(_translate("Dialog", "c"))
        self.bt_OK.setText(_translate("Dialog", "OK"))
        self.bt_STOP.setText(_translate("Dialog", "Отмена"))
