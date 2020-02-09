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

# The name of the file that retains the manual steel list when the app is turned of
st_file_format = "st_log.bbld"


class SteelList:
  def __init__(self):
    self.__obj_steels = {}
    self.__obj_steels_default = Model_MLC.obj_steels_default
    self.__checkLog()

  def __checkLog(self):
    file = pathlib.Path(st_file_format)
    if file.exists():
      subprocess.call(['attrib', '-h', st_file_format])
      f = open(st_file_format, "r")
      d = str(f.read())
      try:
        self.__obj_steels = eval(d)
      except SyntaxError:
        pass
      f.close()
      subprocess.call(['attrib', '+h', st_file_format])

  def ad_st_in_ob(self, st_name, st_sig, st_a, st_b, st_c):
    self.__obj_steels[str(st_name)] = [float(st_sig), float(st_a), float(st_b), float(st_c)]

  def set_st_list(self, x):
    b = eval(x)
    for i in b:
      self.__obj_steels[i] = [b[i][0], b[i][1], b[i][2], b[i][3]]

  def clear_steel_set(self):
    self.__obj_steels.clear()

  def get_obj_steels(self):
    return self.__obj_steels

  def get_obj_steels_default(self):
    return self.__obj_steels_default


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


class add_new_steel(QtWidgets.QDialog):
  def __init__(self, parent, steel_obj):
    super().__init__(parent=None)
    self.steel_obj = steel_obj
    self.ui = UD()
    self.ui.setupUi(self)
    self.ui.bt_OK.clicked.connect(self.acceptd)
    self.ui.bt_STOP.clicked.connect(self.close)

  def acceptd(self):
    print(self.ui.sig_in_2.text())
    new_st_name = self.ui.sig_in_2.text()
    new_st_sig = self.ui.sig_in.text()
    new_st_a = self.ui.a_in.text()
    new_st_b = self.ui.b_in.text()
    new_st_c = self.ui.c_in.text()
    self.steel_obj.ad_st_in_ob(new_st_name, new_st_sig, new_st_a, new_st_b, new_st_c)
    self.close()
    print(self.steel_obj.get_obj_steels())


class steel_set(QtWidgets.QDialog):
  def __init__(self, parent, steel_obj):
    super().__init__(parent=None)
    self.ui = SteelSet()
    self.ui.setupUi(self)
    self.steel_obj = steel_obj
    self.ui.set_cancel.clicked.connect(self.close)
    self.ui.clear_list.clicked.connect(self.clear)
    self.ui.load_list.clicked.connect(self.add_list)
    self.ui.export_list.clicked.connect(self.exp_list)

  def exp_list(self):
    try:
      options = QtWidgets.QFileDialog.Options()
      self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить в...", "default_steel_list",
                                                               "BBLD (*.bbld)", options=options)
      if self.fileName:
        self.writeFile = open(self.fileName, 'w', encoding='utf-8')
        self.writeFile.write(str(self.steel_obj.get_obj_steels()))
        self.writeFile.close()
        self.close()
    except FileNotFoundError:
      pass

  def add_list(self):
    options = QtWidgets.QFileDialog.Options()
    self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Загрузить стали из...", "",
                                                             "BBLD (*.bbld)", options=options)
    if self.fileName:
      format = str(self.fileName).split(".")
      if "bbld" in format or "" in format:
        self.openFile = open(self.fileName, 'r', encoding='utf-8')
        self.readFile = self.openFile.read()
        self.steel_obj.set_st_list(self.readFile)
        self.openFile.close()
        self.close()
      else:
        QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный формат файла",
                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
        pass

  def clear(self):
    res = QtWidgets.QMessageBox.question(self, "Подтвердить удаление?",
                                         "Вы действительно хотите удалить все, вручную введенные, стали?\n"
                                         "(Данное действие необратимо!)", QtWidgets.QMessageBox.Yes |
                                         QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
    if res == QtWidgets.QMessageBox.Yes:
      subprocess.call(['attrib', '-h', st_file_format])
      f = open(st_file_format, "w+")
      f.write("")
      f.close()
      subprocess.call(['attrib', '+h', st_file_format])
      self.steel_obj.clear_steel_set()
      QtWidgets.QMessageBox.information(self, "Сообщение", "Все вручную введенные стали были удалены!",
                                        QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
      self.close()


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

###################################################################


###################################################################


""" MAIN WINDOW """


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
    self.steels = SteelList()
    self.turned_on()
    self.refresh()
    # disable btn_set_colib
    self.disable_btn_set_colib()
    # on click get_calka
    self.ui.btn_set_colib.clicked.connect(self.get_calka)
    # event for button "Расчет"
    self.ui.btn_count.clicked.connect(self.count_main)
    # event if combobox set_colib is changed
    self.ui.comboBox_5.currentIndexChanged.connect(self.disable_btn_set_colib)
    self.ui.comboBox_4.currentIndexChanged.connect(self.disable_discard_steel_btn)
    self.disable_discard_steel_btn()
    self.ui.btn_get_pdf.clicked.connect(self.openDialog)
    self.ui.btn_get_excel.clicked.connect(self.get_ex)
    self.ui.add_steel.clicked.connect(self.ad_st)
    self.ui.discard_steel.clicked.connect(self.remove_st)
    self.ui.btn_refresh.clicked.connect(self.set_st)

    #########################################
    # The testing section (change it when the app is ready!!!!!)
    self.ui.comboBox_5.setDisabled(True)
    self.ui.btn_get_excel.setDisabled(True)
    self.ui.btn_get_pdf.setDisabled(True)
    self.ui.label_17.setText("<html><head/><img src='Лого РосНИТИ рус.png' width=71 height=91/></html>")
    self.ui.label_18.setText("<html><head/><img src='vtz_logo — копия.jpg' width=71 height=91/></html>")
    #########################################

    ###################################################
    # the following code is used to show the FREAKING graph!!!
    self.P1f = DynamicGraph(self)
    self.stack = QtWidgets.QStackedWidget(self)
    self.stack.addWidget(self.P1f)
    lay = QtWidgets.QVBoxLayout(self.ui.listWidget)
    lay.setContentsMargins(0, 0, 0, 0)
    lay.addWidget(self.stack)
    self.toolbar = NavigationToolbar(self.P1f, self)
    lay.addWidget(self.toolbar)
    #########################################

  def closeEvent(self, e):
    res = QtWidgets.QMessageBox.question(self, "Подтвердить выход?",
                                         "Вы действительно хотите закрыть программу?\n"
                                         "(Все несохраненные данные будут потеряны!)", QtWidgets.QMessageBox.Yes |
                                         QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
    if res == QtWidgets.QMessageBox.Yes:
      e.accept()
    else:
      e.ignore()

  def turned_on(self):
    self.ui.comboBox_4.clear()
    arr_default = []
    arr_manual = []
    for key in self.steels.get_obj_steels_default():
      arr_default.append(key)
    if self.steels.get_obj_steels():
      for key in self.steels.get_obj_steels():
        arr_manual.append(key)
    i = 0
    while i < len(arr_default):
      self.ui.comboBox_4.addItem(arr_default[i])
      i += 1
    i = 0
    while i < len(arr_manual):
      self.ui.comboBox_4.addItem(arr_manual[i])
      i += 1

  def refresh(self):
    self.ui.comboBox_4.clear()
    arr_default = []
    arr_manual = []
    for key in self.steels.get_obj_steels_default():
      arr_default.append(key)
    for key in self.steels.get_obj_steels():
      arr_manual.append(key)
    i = 0
    while i < len(arr_default):
      self.ui.comboBox_4.addItem(arr_default[i])
      i += 1
    i = 0
    while i < len(arr_manual):
      self.ui.comboBox_4.addItem(arr_manual[i])
      i += 1
    subprocess.call(['attrib', '-h', st_file_format])
    f = open(st_file_format, "w+")
    f.write(str(self.steels.get_obj_steels()))
    print(str(self.steels.get_obj_steels()))
    f.close()
    subprocess.call(['attrib', '+h', st_file_format])

  def set_st(self):
    dialog_set_st = steel_set(self, self.steels)
    dialog_set_st.exec_()
    self.refresh()

  def ad_st(self):
    dialog_ad_st = add_new_steel(self, self.steels)
    dialog_ad_st.exec_()
    self.refresh()

  def remove_st(self):
    item = str(self.ui.comboBox_4.currentText())
    if item in self.steels.get_obj_steels():
      self.steels.get_obj_steels().pop(item)
      self.refresh()

  def disable_discard_steel_btn(self):
    item = str(self.ui.comboBox_4.currentText())
    if item in self.steels.get_obj_steels():
      self.ui.discard_steel.setEnabled(True)
    else:
      self.ui.discard_steel.setEnabled(False)

  def openDialog(self):
    dialog = Chose_dict_1(self)
    dialog.exec_()

  def get_ex(self):
    for_get_ex()

  # if combobox set_colib is changed
  def disable_btn_set_colib(self):
    q = str(self.ui.comboBox_5.currentText())
    if q != 'Штатная':
      self.ui.btn_set_colib.setEnabled(True)
      self.ui.btn_count.setEnabled(False)
    else:
      self.ui.btn_set_colib.setEnabled(False)
      self.ui.btn_count.setEnabled(True)

  def get_calka(self):
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
      arr_out_math = Model_MLC.math_model(f_D1, f_Doh, f_T, f_beta, f_Dvp, f_nd,
                                          key, self.steels.get_obj_steels())

      # count length of forged billet
      bil_len = float(self.ui.spinBox.text())
      mu = (math.pi * float(f_D1) ** 2) / (math.pi * float(f_Doh) ** 2)
      print(f"Mu = {mu}")
      forged_bil_len = bil_len * mu

      # show required values in the interface
      if arr_out_math[0] != 1111:
        # 1111 is appended to the array in case of an error
        # the next value in array (index = 1) is the error message
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
        self.ui.get_PC1.setText(str(arr_out_math[0]))
        self.ui.get_PC2.setText(str(arr_out_math[1]))
        self.ui.get_forged_len.setText(str(forged_bil_len))
        self.P1f.update_figure(arr_out_math[0], arr_out_math[1])
      else:
        # error message in case of an error
        QtWidgets.QMessageBox.warning(self, "Ошибка", arr_out_math[1],
                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    # count for the other colib_set
    else:
      a = self.get_colib_from_ex_2()
      # get values from interface
      f_D1 = (self.ui.ent_D1.currentText())
      f_Doh = self.ui.ent_Doh.currentText()
      f_T = self.ui.ent_T.text()
      f_beta = self.ui.ent_beta.currentText()
      f_Dvp = self.ui.ent_Dvp.text()
      f_nd = self.ui.ent_nd.text()
      key = str(self.ui.comboBox_4.currentText())
      # use math_model to get required values PC_1 and PC_2
      arr_out_math = Model_MLC.math_model(f_D1, f_Doh, f_T, f_beta, f_Dvp, f_nd,
                                          key, self.steels.get_obj_steels(), a)

      # count length of forged billet
      bil_len = float(self.ui.spinBox.text())
      mu = (math.pi * float(f_D1) ** 2) / (math.pi * float(f_Doh) ** 2)
      print(f"Mu = {mu}")
      forged_bil_len = bil_len * mu

      # show required values in the interface
      if arr_out_math[0] != 1111:
        # 1111 is appended to the array in case of an error
        # the next value in array (index = 1) is the error message
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
        self.ui.get_PC1.setText(str(arr_out_math[0]))
        self.ui.get_PC2.setText(str(arr_out_math[1]))
        self.ui.get_forged_len.setText(str(forged_bil_len))
        self.P1f.update_figure(arr_out_math[0], arr_out_math[1])
      else:
        # error message in case of an error
        QtWidgets.QMessageBox.warning(self, "Ошибка", arr_out_math[1],
                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

      print('not yet')


def main():
  app = QtWidgets.QApplication(sys.argv)
  # app.setQuitOnLastWindowClosed(False)
  window = Prog_comp_1()
  window.show()
  app.exec_()


if __name__ == '__main__':
  main()

