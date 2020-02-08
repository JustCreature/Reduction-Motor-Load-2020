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


class DynamicGraph(FigureCanvas):
  def __init__(self, parent=None, PC1=0, PC2=0):
    fig = Figure()
    self.axes = fig.add_subplot(111)
    self.PC1 = PC1
    self.PC2 = PC2

    self.compute_initial_figure(self.PC1, self.PC2)

    FigureCanvas.__init__(self, fig)
    self.setParent(parent)

    FigureCanvas.setSizePolicy(self,
                               QtWidgets.QSizePolicy.Expanding,
                               QtWidgets.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  def compute_initial_figure(self, pc1, pc2):
    if pc1 != 0 and pc2 != 0:
      p1 = pc1 * 1000
      p2 = pc2 * 1000
      t = p1
      y = 20
      u = 100
      data = (0, p1 - 800, p1, t + random.randint(y, u), t - random.randint(y, u),
              t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
              t - random.randint(y, u), t + random.randint(y, u), t - random.randint(y, u),
              t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
              t - random.randint(y, u), 60, 0)
      t = p2
      data1 = (0, 30, p2, t + random.randint(y, u), t - random.randint(y, u),
               t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
               t - random.randint(y, u), t + random.randint(y, u), t - random.randint(y, u),
               t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
               t - random.randint(y, u), 60, 0)
      # fig, self.axes = plt.subplots()
      bins = (0, 0.4, 0.8, 1.2, 2.5, 3.9, 6.5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
      bins1 = (0, 0.5, 1.3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
      self.axes.plot(bins, data, bins1, data1, label=('x', 'y'))
      self.axes.legend(loc=('upper left'))

  def update_figure(self, pc1, pc2):
    self.axes.cla()
    self.compute_initial_figure(pc1, pc2)
    self.draw()




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










