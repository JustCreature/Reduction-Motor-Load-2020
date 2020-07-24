# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'steel_inp_set.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(452, 123)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.load_list = QtWidgets.QPushButton(Dialog)
        self.load_list.setGeometry(QtCore.QRect(20, 50, 201, 23))
        self.load_list.setObjectName("load_list")
        self.export_list = QtWidgets.QPushButton(Dialog)
        self.export_list.setGeometry(QtCore.QRect(230, 50, 201, 23))
        self.export_list.setObjectName("export_list")
        self.set_cancel = QtWidgets.QPushButton(Dialog)
        self.set_cancel.setGeometry(QtCore.QRect(230, 80, 201, 23))
        self.set_cancel.setObjectName("set_cancel")
        self.clear_list = QtWidgets.QPushButton(Dialog)
        self.clear_list.setGeometry(QtCore.QRect(20, 80, 201, 23))
        self.clear_list.setObjectName("clear_list")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 411, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Настройки списка сталей"))
        self.load_list.setText(_translate("Dialog", "Загрузить список сталей из файла"))
        self.export_list.setText(_translate("Dialog", "Сохранить список сталей в файл"))
        self.set_cancel.setText(_translate("Dialog", "Отмена"))
        self.clear_list.setText(_translate("Dialog", "Очистить список сталей"))
        self.label.setText(_translate("Dialog", "Выберите действие"))
import source_rc
