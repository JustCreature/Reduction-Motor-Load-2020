# Interface imports
from PyQt5 import QtWidgets, QtGui, QtCore
# Main window
from prog_rasch_interface_v6 import Ui_MainWindow
# For getting colib data from Excel
from chose_dict_data_v2 import Ui_Dialog
# Steel input dialog
from steel_inp22222 import Ui_Dialog as UD
# Steel list settings dialog
from steel_inp_set import Ui_Dialog as SteelSet

# All modules import
import math
import sys
import xlrd
import xlwt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure
import random
import pathlib
import subprocess
from math_model import Model_MLC


class Prog_comp_1(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    # event for button "Расчет"
    self.ui.btn_count.clicked.connect(self.count_main)

  def closeEvent(self, e):
    """This method require an affirmation on close event"""
    res = QtWidgets.QMessageBox.question(self, "Подтвердить выход?",
                                         "Вы действительно хотите закрыть программу?\n"
                                         "(Все несохраненные данные будут потеряны!)", QtWidgets.QMessageBox.Yes |
                                         QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
    if res == QtWidgets.QMessageBox.Yes:
      e.accept()
    else:
      e.ignore()

  # btn_count click function
  def count_main(self):
    # count for "Штатная" colib_set
    q = str(self.ui.comboBox_5.currentText())
    if q == 'Штатная':
      ## a = get_colib_from_ex_1()
      # get values from interface
      f_D1 = (self.ui.ent_D1.currentText())
      f_Doh = self.ui.ent_Doh.currentText()
      f_T = self.ui.ent_T.text()
      f_beta = self.ui.ent_beta.currentText()
      f_Dvp = self.ui.ent_Dvp.text()
      f_nd = self.ui.ent_nd.text()
      key = str(self.ui.comboBox_4.currentText())
      print("q")
      # use math_model to get required values PC_1 and PC_2
      arr_out_math = Model_MLC.math_model(f_D1, f_Doh, f_T, f_beta, f_Dvp, f_nd, key)
      if arr_out_math[0] != 1111:
        # 1111 is appended to the array in case of an error
        # the next value in array (index = 1) is the error message
        self.ui.get_PC1.setText(str(arr_out_math[0]))
        self.ui.get_PC2.setText(str(arr_out_math[1]))
      else:
        # error message in case of an error
        QtWidgets.QMessageBox.warning(self, "Ошибка", arr_out_math[1],
                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
    else:
      ## a = get_colib_from_ex_1()
      # get values from interface
      f_D1 = (self.ui.ent_D1.currentText())
      f_Doh = self.ui.ent_Doh.currentText()
      f_T = self.ui.ent_T.text()
      f_beta = self.ui.ent_beta.currentText()
      f_Dvp = self.ui.ent_Dvp.text()
      f_nd = self.ui.ent_nd.text()
      key = str(self.ui.comboBox_4.currentText())
      print("q")
      # use math_model to get required values PC_1 and PC_2
      arr_out_math = Model_MLC.math_model(f_D1, f_Doh, f_T, f_beta, f_Dvp, f_nd,
                                          key, self.steels.get_obj_steels())
      if arr_out_math[0] != 1111:
        # 1111 is appended to the array in case of an error
        # the next value in array (index = 1) is the error message
        self.ui.get_PC1.setText(str(arr_out_math[0]))
        self.ui.get_PC2.setText(str(arr_out_math[1]))
      else:
        # error message in case of an error
        QtWidgets.QMessageBox.warning(self, "Ошибка", arr_out_math[1],
                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
      print('not yet')







def main():
  app = QtWidgets.QApplication(sys.argv)
  window = Prog_comp_1()
  window.show()
  app.exec_()

if __name__ == '__main__':
  main()










