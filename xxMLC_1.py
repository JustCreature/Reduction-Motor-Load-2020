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

# Excel REPORT
def for_get_ex():
  wb = xlwt.Workbook()
  sh = wb.add_sheet('test')
  sh.write(0,0,111)
  wb.save('output.xls')


class Chose_dict_1(QtWidgets.QDialog):
  def __init__(self, parent=None):
    super(Chose_dict_1, self).__init__(parent)
    self.ui = Ui_Dialog()
    self.ui.setupUi(self)


class Prog_comp_1(QtWidgets.QMainWindow):
  # Dict with all parameters
  @staticmethod
  def get_colib_from_ex_2():
    calka = {}
    wb = xlrd.open_workbook('for_Dict_2.xlsx')
    sh = wb.sheet_by_index(0)
    n = 2

    # Add all for a
    for ind_colib_prop in range(1, 4):  # layer for properties (a, b, c)
      # choose property
      if ind_colib_prop == 1:
        colib_prop = '_a'
      elif ind_colib_prop == 2:
        colib_prop = '_b'
      elif ind_colib_prop == 3:
        colib_prop = '_c'
      # choose "beta" angle
      for n in range(2, 57):
        if n < 9:
          beta = 14
        elif n < 16:
          beta = 13
        elif n < 23:
          beta = 12
        elif n < 30:
          beta = 11
        elif n < 37:
          beta = 10
        elif n < 44:
          beta = 9
        elif n < 51:
          beta = 8
        elif n < 57:
          beta = 7
        # add all property's values to the dict {calka}
        for i in range(n, n + 5):
          if str(sh.cell(n, 0).value) == '':
            continue
          key_name = str(sh.cell(n, 0).value) + str(beta) + colib_prop
          key_value = sh.cell(n, ind_colib_prop).value
          calka[key_name] = float(key_value)
          i += 1

        n += 7
      ind_colib_prop += 1
    print(calka)
    return calka

  def __init__(self):
    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    # event for button "Расчет"
    self.ui.btn_count.clicked.connect(self.count_main)
    self.disable_btn_set_colib()
    self.ui.comboBox_5.currentIndexChanged.connect(self.disable_btn_set_colib)


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

  # if combobox set_colib is changed
  def disable_btn_set_colib(self):
    q = str(self.ui.comboBox_5.currentText())
    if q != 'Штатная':
      self.ui.btn_set_colib.setEnabled(True)
      self.ui.btn_count.setEnabled(False)
    else:
      self.ui.btn_set_colib.setEnabled(False)
      self.ui.btn_count.setEnabled(True)

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

      # count length of forged billet
      bil_len = float(self.ui.spinBox.text())
      mu = (math.pi * float(f_D1) ** 2) / (math.pi * float(f_Doh) ** 2)
      print(f"Mu = {mu}")
      forged_bil_len = bil_len * mu

      if arr_out_math[0] != 1111:
        if arr_out_math[0] >= 3.52:
          # if the value of PC1 is greater than allowed
          self.ui.get_PC1.setStyleSheet('background-color: rgb(255, 0, 0); '
                                        'color: rgb(255, 255, 255);')
          QtWidgets.QMessageBox.warning(self, "Внимание!!!", "Превышение максимально "
                                                             "допустимой токовой нагрузки PC №1!",
                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
          self.ui.get_PC1.setStyleSheet('background-color: rgb(255, 255, 255); '
                                        'color: rgb(0, 0, 0);')
        if arr_out_math[1] >= 3.84:
          # if the value of PC2 is greater than allowed
          self.ui.get_PC2.setStyleSheet('background-color: rgb(255, 0, 0); '
                                        'color: rgb(255, 255, 255);')
          QtWidgets.QMessageBox.warning(self, "Внимание!!!", "Превышение максимально "
                                                             "допустимой токовой нагрузки PC №2!",
                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
          self.ui.get_PC2.setStyleSheet('background-color: rgb(255, 255, 255); '
                                        'color: rgb(0, 0, 0);')
        # 1111 is appended to the array in case of an error
        # the next value in array (index = 1) is the error message
        self.ui.get_PC1.setText(str(arr_out_math[0]))
        self.ui.get_PC2.setText(str(arr_out_math[1]))
        self.ui.get_forged_len.setText(str(forged_bil_len))
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

      # count length of forged billet
      bil_len = float(self.ui.spinBox.text())
      mu = (math.pi * float(f_D1) ** 2) / (math.pi * float(f_Doh) ** 2)
      print(f"Mu = {mu}")
      forged_bil_len = bil_len * mu

      if arr_out_math[0] != 1111:
        if arr_out_math[0] >= 3.52:
          # if the value of PC1 is greater than allowed
          self.ui.get_PC1.setStyleSheet('background-color: rgb(255, 0, 0); '
                                        'color: rgb(255, 255, 255);')
          QtWidgets.QMessageBox.warning(self, "Внимание!!!", "Превышение максимально "
                                                             "допустимой токовой нагрузки PC №1!",
                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
          self.ui.get_PC1.setStyleSheet('background-color: rgb(255, 255, 255); '
                                        'color: rgb(0, 0, 0);')
        if arr_out_math[1] >= 3.84:
          # if the value of PC2 is greater than allowed
          self.ui.get_PC2.setStyleSheet('background-color: rgb(255, 0, 0); '
                                        'color: rgb(255, 255, 255);')
          QtWidgets.QMessageBox.warning(self, "Внимание!!!", "Превышение максимально "
                                                             "допустимой токовой нагрузки PC №2!",
                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        else:
          self.ui.get_PC2.setStyleSheet('background-color: rgb(255, 255, 255); '
                                        'color: rgb(0, 0, 0);')
        # 1111 is appended to the array in case of an error
        # the next value in array (index = 1) is the error message
        self.ui.get_PC1.setText(str(arr_out_math[0]))
        self.ui.get_PC2.setText(str(arr_out_math[1]))
        self.ui.get_forged_len.setText(str(forged_bil_len))
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










