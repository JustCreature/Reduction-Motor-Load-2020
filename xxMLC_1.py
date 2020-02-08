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


def main():
  app = QtWidgets.QApplication(sys.argv)
  window = Prog_comp_1()
  window.show()
  app.exec_()

if __name__ == '__main__':
  main()










