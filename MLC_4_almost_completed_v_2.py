# Interface imports
from PyQt5 import QtWidgets, QtGui, QtCore, QtPrintSupport
# Main window
from prog_rasch_interface_v12 import Ui_MainWindow
# Steel input dialog
from steel_input import Ui_Dialog as UD
# Steel list settings dialog
from steel_inp_set import Ui_Dialog as SteelSet

from PyQt5.QtCore import QTranslator, QLocale

I18N_QT_PATH = ':/translations/translations/'

# All modules import
import sys
import time
import base64
import xlrd
import xlwt
import tempfile
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import random
import pathlib
import subprocess
from math_model_v2 import Model_MLC
import os
import matplotlib
import datetime
matplotlib.use("Agg")
from matplotlib.figure import Figure
import source_rc

# The name of the file that retains the manual steel list when the app is turned of
user_path = os.path.expanduser("~")
steel_file = os.path.join(user_path, "st_log.bbld")
# File for collecting data of usage
data_file = os.path.join(user_path, "data_log.bbld")

if pathlib.Path(steel_file).exists():
    subprocess.call(['attrib', '-h', steel_file])
if pathlib.Path(data_file).exists():
    subprocess.call(['attrib', '-h', data_file])

class SteelList:
    """SteelList is the class that creates the object of all manually inputed steel grades"""
    def __init__(self):
        self.__obj_steels = {}
        self.__obj_steels_default = Model_MLC.obj_steels_default
        self.__check_log()

    def __check_log(self):
        """The method that checks weather manually inputted steels exist
        (if the file which stores them does exist) and if they do puts them in the dict
        (this method is called by the constructor)"""
        file = pathlib.Path(steel_file)
        if file.exists():

            f = open(steel_file, "r")
            d = str(f.read())
            try:
                self.__obj_steels = eval(d)
            except SyntaxError:
                pass
            f.close()


    def add_steel_in_ob(self, steel_name, steel_sig, steel_a, steel_b, steel_c):
        """This method adds new steel grade to the dict"""
        self.__obj_steels[str(steel_name)] = [float(steel_sig), float(steel_a), float(steel_b), float(steel_c)]

    def remove_steel(self, steel_name):
        self.__obj_steels.pop(steel_name)

    def set_steel_list(self, x):
        """This method imports the list of steel grades from outer file"""
        b = eval(x)
        for i in b:
            self.__obj_steels[i] = [b[i][0], b[i][1], b[i][2], b[i][3]]

    def clear_steel_list(self):
        """Delete all items from the steel list"""
        self.__obj_steels.clear()

    def get_obj_steels(self):
        """This method returns the list of inputted manually steel grades"""
        return self.__obj_steels

    def get_obj_steels_default(self):
        """This method returns the list of default steel grades"""
        return self.__obj_steels_default


# Excel REPORT
class GetExcelFile(QtWidgets.QDialog):
    """Create report in .xls format"""
    def __init__(self, parent, array_with_results, arr_parameters, which_button):
        super().__init__(parent=None)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('report')
        sheet.write(0, 0, "Date:")
        now = datetime.datetime.now().strftime("%d-%m-%Y %H--%M")
        sheet.write(0, 1, now)
        sheet.write(0, 3, "Калибровка")
        sheet.write(0, 4, array_with_results[0])
        # sheet.write(3, 1, "Исходдные данные:")
        subhead_title_style = xlwt.easyxf('font: bold 1')


        sheet.write_merge(3, 3, 0, 4, "Исходдные данные:", subhead_title_style)
        sheet.write_merge(5, 5, 0, 3, "Диаметр исходной заготовки, мм")
        sheet.write(5, 4, int(arr_parameters[0]))
        sheet.write_merge(7, 7, 0, 3, "Длина исходной заготовки, мм")
        sheet.write(7, 4, int(arr_parameters[1]))
        sheet.write_merge(9, 9, 0, 3, "Диаметр обжатой заготовки, мм")
        sheet.write(9, 4, int(arr_parameters[2]))
        sheet.write_merge(11, 11, 0, 3, "Исходная температура, град цельс")
        sheet.write(11, 4, int(arr_parameters[3]))
        sheet.write_merge(13, 13, 0, 3, "Угол подачи, град")
        sheet.write(13, 4, int(arr_parameters[4]))
        sheet.write_merge(15, 15, 0, 3, "Диаметр валков в пережиме, мм")
        sheet.write(15, 4, int(arr_parameters[5]))
        sheet.write_merge(17, 17, 0, 3, "Частота вращения двигателя, мин -1")
        sheet.write(17, 4, int(arr_parameters[6]))
        sheet.write_merge(19, 19, 0, 3, "Марка стали")
        sheet.write(19, 4, arr_parameters[7], xlwt.easyxf('align: horiz right'))

        sheet.write_merge(22, 22, 0, 4, "Результаты:", subhead_title_style)
        sheet.write_merge(24, 24, 0, 3, "PC1, А")
        sheet.write(24, 4, array_with_results[1])
        sheet.write_merge(26, 26, 0, 3, "PC2, А")
        sheet.write(26, 4, array_with_results[2])
        sheet.write_merge(28, 28, 0, 3, "Длина обжатой заготовки, мм")
        sheet.write(28, 4, array_with_results[3])

        try:
            if which_button == 1:
                # ONLY save excel file to the directory RML_log (or create directory unless it exists)
                log_dir_path = os.path.dirname(os.path.realpath(__file__)) + "/RML_log"
                if not os.path.exists(log_dir_path):
                    os.makedirs("RML_log")
                excel_file_name = log_dir_path + '/output' + datetime.datetime.now().strftime("%d.%m.%y__%H_%M_%S") \
                                  + f"__{arr_parameters[0]}-{arr_parameters[2]}-{arr_parameters[6]}-{arr_parameters[7]}" + ".xls"
                workbook.save(excel_file_name)
            elif which_button == 2:
                # create and open temporary file .xls
                temp = tempfile.TemporaryFile().name + ".xls"
                workbook.save(temp)
                os.startfile(temp)
            else:
                # save and open excel file
                log_dir_path = os.path.dirname(os.path.realpath(__file__)) + "/RML_log"
                if not os.path.exists(log_dir_path):
                    os.makedirs("RML_log")
                excel_file_name = log_dir_path + '/output' + datetime.datetime.now().strftime("%d.%m.%y__%H_%M_%S") \
                                  + f"__{arr_parameters[0]}-{arr_parameters[2]}-{arr_parameters[6]}-{arr_parameters[7]}" \
                                  + ".xls"
                workbook.save(excel_file_name)
                os.startfile(excel_file_name)

        except PermissionError:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Закройте файл .xls!!!",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)


class AddNewSteel(QtWidgets.QDialog):
    """This class is a dialog window that is used to input new steel grade"""
    def __init__(self, parent, steel_obj):
        """This is the constructor that gets 1 argument which is
        the list of steel grades of SteelList instance"""
        super().__init__(parent=None)
        self.steel_obj = steel_obj
        self.ui = UD()
        self.ui.setupUi(self)
        self.ui.bt_OK.clicked.connect(self.acceptd)
        self.ui.bt_STOP.clicked.connect(self.close)

    def acceptd(self):
        """The method that is used when Ok button is pressed"""
        new_st_name = self.ui.sig_in_2.text()
        new_st_sig = self.ui.sig_in.text()
        new_st_a = self.ui.a_in.text()
        new_st_b = self.ui.b_in.text()
        new_st_c = self.ui.c_in.text()

        if new_st_sig.find(",") != -1:
            new_st_sig = new_st_sig.replace(",", ".")
        if new_st_a.find(",") != -1:
            new_st_a = new_st_a.replace(",", ".")
        if new_st_b.find(",") != -1:
            new_st_b = new_st_b.replace(",", ".")
        if new_st_c.find(",") != -1:
            new_st_c = new_st_c.replace(",", ".")

        self.steel_obj.add_steel_in_ob(new_st_name, new_st_sig, new_st_a, new_st_b, new_st_c)
        self.close()


class SteelSettings(QtWidgets.QDialog):
    """This class is a dialog window that is used to customise the list of steel grades"""
    def __init__(self, parent, steel_obj):
        super().__init__(parent=None)
        self.ui = SteelSet()
        self.ui.setupUi(self)
        self.steel_obj = steel_obj
        self.ui.set_cancel.clicked.connect(self.close)
        self.ui.clear_list.clicked.connect(self.clear_list)
        self.ui.load_list.clicked.connect(self.import_list)
        self.ui.export_list.clicked.connect(self.export_list)

    def export_list(self):
        """The method allows to export the list of steel grades to outer file"""
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

    def import_list(self):
        """The method allows to choose the outer file to import the list of steel grades"""
        options = QtWidgets.QFileDialog.Options()
        self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Загрузить стали из...", "",
                                                                 "BBLD (*.bbld)", options=options)
        if self.fileName:
            file_type = str(self.fileName).split(".")
            if "bbld" in file_type:
                self.openFile = open(self.fileName, 'r', encoding='utf-8')
                self.readFile = self.openFile.read()
                try:
                    self.steel_obj.set_steel_list(self.readFile)
                    QtWidgets.QMessageBox.information(self, "Сообщение", "Список сталей загружен.",
                                                      QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                except SyntaxError:
                    QtWidgets.QMessageBox.warning(self, "Ошибка", "Данный файл не может быть использован.\n"
                                                                  "Возможно файл был поврежден!!!\nВыберите другой файл.",
                                                  QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                self.openFile.close()
                self.close()
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка", "Неверный формат файла",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                pass

    def clear_list(self):
        """The method allows to clear the list of steel grades"""
        res = QtWidgets.QMessageBox.question(self, "Подтвердить удаление?",
                                             "Вы действительно хотите удалить все, вручную введенные, стали?\n"
                                             "(Данное действие необратимо!)", QtWidgets.QMessageBox.Yes |
                                             QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if res == QtWidgets.QMessageBox.Yes:

            f = open(steel_file, "w+")
            f.write("")
            f.close()

            self.steel_obj.clear_steel_list()
            QtWidgets.QMessageBox.information(self, "Сообщение", "Все вручную введенные стали были удалены!",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.close()


class BilletGraph(FigureCanvas):
    """A canvas that updates itself when the button 'Расчет'(Count) is pressed with a new plot."""

    def __init__(self, parent=None, pc1=0, pc2=0, reduction_time=0):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_ylabel("Нагрузка, А")
        self.axes.set_xlabel("Время, с")
        self.fig.tight_layout(rect=[0.04, 0.04, 1, 1])
        # in case of any problems with tight_layout USE set_tight_layout
        # self.fig.set_tight_layout(True)
        self.pc1 = pc1
        self.pc2 = pc2
        self.reduction_time = reduction_time

        self.compute_initial_figure(self.pc1, self.pc2, self.reduction_time)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self, pc1, pc2, reduction_time):
        """Method to create the chart"""
        if pc1 != 0 and pc2 != 0:
            pc1 = pc1 * 1000
            pc2 = pc2 * 1000
            t = pc1
            y = 20
            u = 100
            y_pc1 = (0, pc1 - 800, pc1, t + random.randint(y, u), t - random.randint(y, u),
                     t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
                     t - random.randint(y, u), t + random.randint(y, u), t - random.randint(y, u),
                     t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
                     t - random.randint(y, u), 60, 0)

            t = pc2
            y_pc2 = (0, pc2 - 800, pc2, t + random.randint(y, u), t - random.randint(y, u),
                     t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
                     t - random.randint(y, u), t + random.randint(y, u), t - random.randint(y, u),
                     t + random.randint(y, u), t - random.randint(y, u), t + random.randint(y, u),
                     t - random.randint(y, u), 60, 0)

            # x_pc1 = (0, 0.4, 0.8, 1.2, 2.5, 3.9, 6.5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
            # x_pc2 = (0, 0.5, 1.3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
            share = reduction_time / 100
            x_pc1 = (
                0, 2.5 * share, 5 * share, 7.5 * share, 15.625 * share, 24.375 * share, 40.625 * share,
                43.75 * share, 50 * share, 56.25 * share, 62.5 * share, 68.75 * share, 75 * share,
                81.25 * share, 87.5 * share, 93.75 * share, 100 * share
            )
            x_pc2 = (
                0, 3.125 * share, 8.125 * share, 18.7 * share, 25 * share, 31.25 * share, 37.5 * share,
                43.75 * share, 50 * share, 56.25 * share, 62.5 * share, 68.75 * share, 75 * share,
                81.25 * share, 87.5 * share, 93.75 * share, 100 * share
            )

            self.axes.plot(x_pc1, y_pc1, label='PC1')
            self.axes.plot(x_pc2, y_pc2, label='PC2')
            self.axes.legend(loc='best')

    def update_figure(self, pc1, pc2, reduction_time):
        """Method to update the chart"""
        self.axes.cla()
        self.axes.set_ylabel("Нагрузка, А")
        self.axes.set_xlabel("Время, с")
        self.compute_initial_figure(pc1, pc2, reduction_time)
        self.draw()


class AnalysisGraph(FigureCanvas):
    """A canvas that updates itself when the button 'Расчет'(Count) is pressed with a new plot."""

    def __init__(self, parent=None, key_billet="неверной", arr_with_analysis_result=[[1, 1, 1]]):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        self.axes.set_ylabel("Токовая нагрузка, А")
        self.axes.set_xlabel(f"Анализируемый параметр")
        self.fig.tight_layout(rect=[0.04, 0.04, 1, 1])
        # in case of any problems with tight_layout USE set_tight_layout
        # self.fig.set_tight_layout(True)
        self.res = arr_with_analysis_result

        self.compute_initial_figure(self.res)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self, res):
        """Method to create the chart"""
        # some code
        x_pc1 = []
        y_pc1 = []
        x_pc2 = []
        y_pc2 = []

        for item in res:
            x_pc1.append(item[2])
            x_pc2.append(item[2])

            y_pc1.append(item[0] * 1000)
            y_pc2.append(item[1] * 1000)

        self.axes.plot(x_pc1, y_pc1, label='РС1')
        self.axes.plot(x_pc2, y_pc2, label='РС2')
        self.axes.legend(loc='best')

    def update_figure(self, key_billet="неверной", res=[[100, 100, 100]]):
        """Method to update the chart"""
        self.axes.cla()
        self.axes.set_ylabel("Токовая нагрузка, А")
        if key_billet == "forged_chosen":
            self.axes.set_xlabel(f"Диаметр обжатой заготовки, мм")
        elif key_billet == "init_chosen":
            self.axes.set_xlabel(f"Диаметр исходной заготовки, мм")
        elif key_billet == "temp_chosen":
            self.axes.set_xlabel(f"Температура заготовки, \xb0С")
        elif key_billet == "beta_chosen":
            self.axes.set_xlabel(f"Утог подачи, град.")
        elif key_billet == "nd_chosen":
            self.axes.set_xlabel(f"Частота вращения двигателя, мин\u207b\u00b9")
        self.compute_initial_figure(res)
        self.draw()





###################################################################


###################################################################


""" MAIN WINDOW """


class ProgComp1(QtWidgets.QMainWindow):
    """This class represents the main window"""
    # Dict with all parameters
    @staticmethod
    def get_colib_from_excel_2():
        """This method allows to get the colib data from outer .xlsx file"""
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
        """This is a constructor (it dose NOT get any arguments)"""
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.steels = SteelList()
        self.turned_on()
        self.refresh()

        # event for button "Расчет"
        self.ui.btn_count.clicked.connect(self.count_main)
        # event for button "Анализ"
        self.ui.btn_analyze.clicked.connect(self.analyze_main)
        # event if combobox set_colib is changed
        self.ui.choose_steel.currentIndexChanged.connect(self.disable_remove_steel_btn)
        self.ui.choose_steel_a.currentIndexChanged.connect(self.disable_remove_steel_btn)
        self.disable_remove_steel_btn()
        self.ui.btn_save_excel.clicked.connect(self.save_excel)
        self.ui.btn_get_excel.clicked.connect(self.get_excel)
        self.ui.btn_get_and_save_excel.clicked.connect(self.get_and_save_excel)
        self.ui.add_steel.clicked.connect(self.add_steel)
        self.ui.discard_steel.clicked.connect(self.remove_steel)
        self.ui.btn_refresh.clicked.connect(self.set_steel)
        self.ui.add_steel_a.clicked.connect(self.add_steel)
        self.ui.discard_steel_a.clicked.connect(self.remove_steel_a)
        self.ui.btn_refresh_a.clicked.connect(self.set_steel)
        self.array_with_results = []
        self.arr_parameters = []

        #########################################
        # The testing section (change it when the app is ready!!!!!)
        self.ui.btn_get_excel.setDisabled(True)
        self.ui.btn_save_excel.setDisabled(True)
        self.ui.btn_get_and_save_excel.setDisabled(True)
        #########################################

        ###################################################
        # the following code is used to show the FREAKING graph!!!
        self.P1f = BilletGraph(self)
        self.stack = QtWidgets.QStackedWidget(self)
        self.stack.addWidget(self.P1f)
        lay = QtWidgets.QVBoxLayout(self.ui.listWidget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.stack)
        self.toolbar = NavigationToolbar(self.P1f, self)
        lay.addWidget(self.toolbar)
        #########################################

        ###################################################
        # the following code is used to show the FREAKING ANALYSIS graph!!!
        self.A1f = AnalysisGraph(self)
        self.stack_a = QtWidgets.QStackedWidget(self)
        self.stack_a.addWidget(self.A1f)
        lay_a = QtWidgets.QVBoxLayout(self.ui.listWidget_a)
        lay_a.setContentsMargins(0, 0, 0, 0)
        lay_a.addWidget(self.stack_a)
        self.toolbar_a = NavigationToolbar(self.A1f, self)
        lay_a.addWidget(self.toolbar_a)
        #########################################

        ##################################
        self.ui.btn_rosniti_about.clicked.connect(self.about)
        self.ui.btn_vtz_about.clicked.connect(self.about)

        self.ui.frame_with_fact.setDisabled(True)
        self.ui.check_fact.stateChanged.connect(self.disable_frame_with_fact)
        self.ui.frame_with_reduction.setDisabled(True)
        self.ui.check_manual_reduction.stateChanged.connect(self.disable_frame_with_reduction)
        self.ui.frame_with_reduction_a.setDisabled(True)
        self.ui.check_manual_reduction_a.stateChanged.connect(self.disable_frame_with_reduction_a)

        self.ui.btn_secret_behind_vtz_logo.clicked.connect(self.export_usage_data)

        self.ui.choose_colib.currentIndexChanged.connect(self.colib_changed)
        self.ui.choose_colib_a.currentIndexChanged.connect(self.colib_changed_a)
        ###############################

        ########################################
        # Choose fot to analise (radio buttons)
        self.ui.radio_use_init_bil_a.setChecked(True)
        self.radio_choose()
        self.ui.radio_use_init_bil_a.clicked.connect(self.radio_choose)
        self.ui.radio_use_forged_bil_a.clicked.connect(self.radio_choose)
        self.ui.radio_use_temp_bil_a.clicked.connect(self.radio_choose)
        self.ui.radio_use_feed_angle_a.clicked.connect(self.radio_choose)
        self.ui.radio_use_shaft_speed_a.clicked.connect(self.radio_choose)
        ##################################

        self.ui.btn_go_to_analysis.clicked.connect(self.change_tab)


        ########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # Conversion section

        self.spotter = 0
        self.ui.set_piercing_percent.valueChanged.connect(self.convert_to_piercing_mm)
        self.ui.set_piercing_mm.valueChanged.connect(self.convert_to_piercing_percent)
        self.ui.set_colib_mm.valueChanged.connect(self.convert_to_colib_percent)
        self.ui.set_colib_percent.valueChanged.connect(self.convert_to_colib_mm)

        self.ui.set_piercing_percent_a.valueChanged.connect(self.convert_to_piercing_mm_a)
        self.ui.set_piercing_mm_a.valueChanged.connect(self.convert_to_piercing_percent_a)
        self.ui.set_colib_mm_a.valueChanged.connect(self.convert_to_colib_percent_a)
        self.ui.set_colib_percent_a.valueChanged.connect(self.convert_to_colib_mm_a)

        self.convert_to_colib_percent()
        self.convert_to_piercing_mm()

        self.convert_to_colib_percent_a()
        self.convert_to_piercing_mm_a()

        ########@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def colib_changed(self):
        if self.ui.choose_colib.currentText() == '87/17-01.04':
            self.ui.ent_Dvp.setValue(535)
        elif self.ui.choose_colib.currentText() == 'П20.28РН':
            self.ui.ent_Dvp.setValue(485)
        elif self.ui.choose_colib.currentText() == 'П20.28-ТЗ':
            self.ui.ent_Dvp.setValue(535)

    def colib_changed_a(self):
        if self.ui.choose_colib_a.currentText() == '87/17-01.04':
            self.ui.ent_Dvp_a.setValue(535)
        elif self.ui.choose_colib_a.currentText() == 'П20.28РН':
            self.ui.ent_Dvp_a.setValue(485)
        elif self.ui.choose_colib_a.currentText() == 'П20.28-ТЗ':
            self.ui.ent_Dvp_a.setValue(535)

    def change_tab(self):
        """When "Go to Analysis" (Переход к Анализу) button is pressed"""
        # get values from interface
        self.ui.ent_D1_a.setCurrentText(self.ui.ent_D1.currentText())
        self.ui.ent_Doh_a.setCurrentText(self.ui.ent_Doh.currentText())
        self.ui.ent_T_a.setValue(int(self.ui.ent_T.text()))
        self.ui.ent_beta_a.setCurrentText(self.ui.ent_beta.currentText())
        self.ui.ent_Dvp_a.setValue(int(self.ui.ent_Dvp.text()))
        self.ui.ent_nd_a.setValue(int(self.ui.ent_nd.text()))
        self.ui.choose_steel_a.setCurrentText(self.ui.choose_steel.currentText())
        self.ui.ent_billet_length_a.setValue(int(self.ui.ent_billet_length.text()))
        self.ui.choose_colib_a.setCurrentText(self.ui.choose_colib.currentText())

        if self.ui.check_manual_reduction.isChecked():
            self.ui.check_manual_reduction_a.setChecked(True)

            piercing_percent = self.ui.set_piercing_percent.text()
            piercing_mm = self.ui.set_piercing_mm.text()
            colib_mm = self.ui.set_colib_mm.text()
            colib_percent = self.ui.set_colib_percent.text()

            if piercing_percent.find(",") != -1:
                piercing_percent = piercing_percent.replace(",", ".")
            if colib_mm.find(",") != -1:
                colib_mm = colib_mm.replace(",", ".")
            if piercing_mm.find(",") != -1:
                piercing_mm = piercing_mm.replace(",", ".")
            if colib_percent.find(",") != -1:
                colib_percent = colib_percent.replace(",", ".")
            self.ui.set_piercing_percent_a.setValue(float(piercing_percent))
            self.ui.set_colib_mm_a.setValue(float(colib_mm))
            self.ui.set_piercing_mm_a.setValue(float(piercing_mm))
            self.ui.set_colib_percent_a.setValue(float(colib_percent))


        self.ui.tab_analysis.setCurrentIndex(1)


    def radio_choose(self):
        """Changes when radio button choice is changed"""
        if self.ui.radio_use_init_bil_a.isChecked():
            # self.ui.label_forged_diam_a.setDisabled(True)
            self.ui.ent_D1_a.setDisabled(True)
            self.ui.ent_Doh_a.setDisabled(False)
            self.ui.ent_T_a.setDisabled(False)
            self.ui.ent_beta_a.setDisabled(False)
            self.ui.ent_nd_a.setDisabled(False)
            self.ui.label_69.setText(f"График зависимости токовых нагрузок от диаметра исходной заготовки")
            self.ui.label_an.setText(f"Максимально допустимый диаметр исходной заготовки, мм")
            self.key_analysis_for = "init_chosen"
        elif self.ui.radio_use_temp_bil_a.isChecked():
            self.ui.ent_T_a.setDisabled(True)
            self.ui.ent_Doh_a.setDisabled(False)
            self.ui.ent_D1_a.setDisabled(False)
            self.ui.ent_beta_a.setDisabled(False)
            self.ui.ent_nd_a.setDisabled(False)
            self.ui.label_69.setText(f"График зависимости токовых нагрузок от температуры заготовки")
            self.ui.label_an.setText(f"Минимально допустимая температура заготовки, \xb0С")
            self.key_analysis_for = "temp_chosen"
        elif self.ui.radio_use_feed_angle_a.isChecked():
            self.ui.ent_beta_a.setDisabled(True)
            self.ui.ent_T_a.setDisabled(False)
            self.ui.ent_Doh_a.setDisabled(False)
            self.ui.ent_D1_a.setDisabled(False)
            self.ui.ent_nd_a.setDisabled(False)
            self.ui.label_69.setText(f"График зависимости токовых нагрузок от угла подачи")
            self.ui.label_an.setText(f"Максимально допустимый угол подачи, град")
            self.key_analysis_for = "beta_chosen"
        elif self.ui.radio_use_shaft_speed_a.isChecked():
            self.ui.ent_nd_a.setDisabled(True)
            self.ui.ent_beta_a.setDisabled(False)
            self.ui.ent_T_a.setDisabled(False)
            self.ui.ent_Doh_a.setDisabled(False)
            self.ui.ent_D1_a.setDisabled(False)
            self.ui.label_69.setText(f"График зависимости токовых нагрузок от частоты вращения двигателя")
            self.ui.label_an.setText(f"Максимально допустимая частота вращения двигателя, мин\u207b\u00b9")
            self.key_analysis_for = "nd_chosen"
        else:
            # self.ui.label_init_diam_a.setDisabled(True)
            self.ui.ent_Doh_a.setDisabled(True)
            self.ui.ent_D1_a.setDisabled(False)
            self.ui.ent_T_a.setDisabled(False)
            self.ui.ent_beta_a.setDisabled(False)
            self.ui.ent_nd_a.setDisabled(False)
            self.ui.label_69.setText(f"График зависимости токовых нагрузок от диаметра обжатой заготовки")
            self.ui.label_an.setText(f"Минимально допустимый диаметр обжатой заготовки, мм")
            self.key_analysis_for = "forged_chosen"

    def get_data_to_convert(self):
        """Gets data for conversion of one value to another (percent to mm and back)"""
        self.f_D1 = (self.ui.ent_D1.currentText())
        self.f_Doh = self.ui.ent_Doh.currentText()
        if self.f_Doh.find(",") != -1:
            self.f_Doh = self.f_Doh.replace(",", ".")
        self.f_T = self.ui.ent_T.text()
        self.piercing_percent = self.ui.set_piercing_percent.text()
        if self.piercing_percent.find(",") != -1:
            self.piercing_percent = self.piercing_percent.replace(",", ".")
        self.colib_percent = self.ui.set_colib_percent.text()
        if self.colib_percent.find(",") != -1:
            self.colib_percent = self.colib_percent.replace(",", ".")
        self.piercing_mm = self.ui.set_piercing_mm.text()
        if self.piercing_mm.find(",") != -1:
            self.piercing_mm = self.piercing_mm.replace(",", ".")
        self.colib_mm = self.ui.set_colib_mm.text()
        if self.colib_mm.find(",") != -1:
            self.colib_mm = self.colib_mm.replace(",", ".")

        self.piercing_percent_a = self.ui.set_piercing_percent_a.text()
        if self.piercing_percent_a.find(",") != -1:
            self.piercing_percent_a = self.piercing_percent_a.replace(",", ".")
        self.colib_percent_a = self.ui.set_colib_percent_a.text()
        if self.colib_percent_a.find(",") != -1:
            self.colib_percent_a = self.colib_percent_a.replace(",", ".")
        self.piercing_mm_a = self.ui.set_piercing_mm_a.text()
        if self.piercing_mm_a.find(",") != -1:
            self.piercing_mm_a = self.piercing_mm_a.replace(",", ".")
        self.colib_mm_a = self.ui.set_colib_mm_a.text()
        if self.colib_mm_a.find(",") != -1:
            self.colib_mm_a = self.colib_mm_a.replace(",", ".")

    def convert_to_colib_mm(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "colib_percent_to_mm"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(
                self.f_D1, self.f_Doh, self.f_T, self.piercing_percent, self.colib_percent, key
            )
            self.ui.set_colib_mm.setValue(round(convrted[2], 2) * 2)
        else:
            self.spotter = 0

    def convert_to_colib_percent(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "colib_mm_to_percent"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_mm, self.colib_mm, key)
            self.ui.set_colib_percent.setValue(round(convrted[3], 2))
        else:
            self.spotter = 0

    def convert_to_piercing_mm(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "piercing_percent_to_mm"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_percent, self.colib_mm, key)
            self.ui.set_piercing_mm.setValue(round(convrted[0], 2) * 2)
        else:
            self.spotter = 0

    def convert_to_piercing_percent(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "piercing_mm_to_percent"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_mm, self.colib_mm, key)
            self.ui.set_piercing_percent.setValue(round(convrted[1], 2))
        else:
            self.spotter = 0

    def convert_to_colib_mm_a(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "colib_percent_to_mm"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_percent_a, self.colib_percent_a, key)
            self.ui.set_colib_mm_a.setValue(round(convrted[2], 2) * 2)
        else:
            self.spotter = 0

    def convert_to_colib_percent_a(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "colib_mm_to_percent"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_mm_a, self.colib_mm_a, key)
            self.ui.set_colib_percent_a.setValue(round(convrted[3], 2))
        else:
            self.spotter = 0

    def convert_to_piercing_mm_a(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "piercing_percent_to_mm"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_percent_a, self.colib_mm_a, key)
            self.ui.set_piercing_mm_a.setValue(round(convrted[0], 2) * 2)
        else:
            self.spotter = 0

    def convert_to_piercing_percent_a(self):
        if self.spotter == 0:
            self.spotter = 1

            key = "piercing_mm_to_percent"
            self.get_data_to_convert()

            convrted = Model_MLC.covert_mm_to_percent(self.f_D1, self.f_Doh, self.f_T, self.piercing_mm_a, self.colib_mm_a, key)
            self.ui.set_piercing_percent_a.setValue(round(convrted[1], 2))
        else:
            self.spotter = 0

    def about(self):
        """Shows message about the app when one of the logos is clicked"""
        tmk_link = "https://www.tmk-group.ru/"
        rosniti_link = "https://www.tmk-group.ru/rosniti"
        vtz_link = "https://vtz.tmk-group.ru/"
        msg = "Reduction Motor Load - программа предназначеная для " \
              "расчета мощности, необходимой для обжатия заготовок " \
              "из различных марок сталей, и перевода значений мощности " \
              "в токовые нагрузки на приводе трехвалкового " \
              "стана Ассела АО «ВТЗ», а также для расчета длины " \
              "обжатой заготовки. Программа включает в себя " \
              "математическую модель, систему граничных условий и " \
              "информационные данные для выполнения расчетов" \
              "<br><br><br>Авторы:<br><br><br>ОАО «РосНИТИ»<br><br>" \
              "Корсаков Андрей Александрович<br><br>" \
              "Михалкин Дмитрий Владимирович<br><br>" \
              "Заварцев Никита Андреевич<br><br>" \
              "Алютина Екатерина Владимировна<br><br>" \
              "<br>АО «ВТЗ»<br><br>" \
              "Красиков Андрей Владимирович<br><br>" \
              "Тыщук Игорь Николаевич<br><br>" \
              "Ульянов Андрей Георгиевич<br><br>" \
              "Байков Василий Валентинович<br><br>" \
            f"<div><p>ТМК: <a href='{tmk_link}'>https://www.tmk-group.ru/</a></p>" \
            f"<p>РосНИТИ: <a href='{rosniti_link}'>https://www.tmk-group.ru/rosniti</a></p>" \
            f"<p>ВТЗ: <a href='{vtz_link}'>https://vtz.tmk-group.ru/</a></p></div>"

        QtWidgets.QMessageBox.information(self, "О Программе", msg,
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)

    def closeEvent(self, e):
        """This method require an affirmation on close event"""
        res = QtWidgets.QMessageBox.question(self, "Подтвердить выход?",
                                             "Вы действительно хотите закрыть программу?\n"
                                             "(Все несохраненные данные будут потеряны!)", QtWidgets.QMessageBox.Yes |
                                             QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if res == QtWidgets.QMessageBox.Yes:
            # record current data of calculation to data file (or create it if it doesn't exist)

            f = open(data_file, "w")
            encode = base64.b64encode(str.encode(str(self.existing_data)))
            f.write(encode.decode())
            f.close()


            if pathlib.Path(steel_file).exists():
                subprocess.call(['attrib', '+h', steel_file])
            if pathlib.Path(data_file).exists():
                subprocess.call(['attrib', '+h', data_file])
            e.accept()
        else:
            e.ignore()

    def export_usage_data(self):
        """Get the data of user activity to external file"""
        try:
            options = QtWidgets.QFileDialog.Options()
            self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Сохранить в...", "data_log",
                                                                     "BBLD (*.bbld)", options=options)
            if self.fileName:
                self.writeFile = open(self.fileName, "w", encoding='utf-8')
                encode = base64.b64encode(str.encode(str(self.existing_data)))
                self.writeFile.write(encode.decode())
                self.writeFile.close()
        except FileNotFoundError:
            pass

    def turned_on(self):
        """This is a refreshment when the program is turned on"""
        self.ui.choose_steel.clear()
        self.ui.choose_steel_a.clear()
        arr_default = []
        arr_manual = []
        for key in self.steels.get_obj_steels_default():
            arr_default.append(key)
        if self.steels.get_obj_steels():
            for key in self.steels.get_obj_steels():
                arr_manual.append(key)
        i = 0
        while i < len(arr_default):
            self.ui.choose_steel.addItem(arr_default[i])
            self.ui.choose_steel_a.addItem(arr_default[i])
            i += 1
        i = 0
        while i < len(arr_manual):
            self.ui.choose_steel.addItem(arr_manual[i])
            self.ui.choose_steel_a.addItem(arr_manual[i])
            i += 1

        try:
            # look if there is a data file and if it does get the array. If it doesn't, create the empty one

            f = open(data_file, "r")
            decode = base64.b64decode(str.encode(f.read()))
            self.existing_data = eval(decode.decode())
            # self.existing_data = eval(f.read())
            f.close()

        except FileNotFoundError:
            self.existing_data = []

    def refresh(self):
        """This is a refreshment when something is changed"""
        self.ui.choose_steel.clear()
        self.ui.choose_steel_a.clear()
        arr_default = []
        arr_manual = []
        for key in self.steels.get_obj_steels_default():
            arr_default.append(key)
        for key in self.steels.get_obj_steels():
            arr_manual.append(key)
        i = 0
        while i < len(arr_default):
            self.ui.choose_steel.addItem(arr_default[i])
            self.ui.choose_steel_a.addItem(arr_default[i])
            i += 1
        i = 0
        while i < len(arr_manual):
            self.ui.choose_steel.addItem(arr_manual[i])
            self.ui.choose_steel_a.addItem(arr_manual[i])
            i += 1

        f = open(steel_file, "w+")
        f.write(str(self.steels.get_obj_steels()))
        f.close()


    def disable_frame_with_fact(self):
        if not self.ui.check_fact.isChecked():
            self.ui.frame_with_fact.setDisabled(True)
        else:
            self.ui.frame_with_fact.setDisabled(False)

    def disable_frame_with_reduction(self):
        if not self.ui.check_manual_reduction.isChecked():
            self.ui.set_piercing_percent.setValue(2.00)
            self.ui.set_colib_mm.setValue(3.00)
            self.ui.frame_with_reduction.setDisabled(True)
        else:
            self.ui.frame_with_reduction.setDisabled(False)

    def disable_frame_with_reduction_a(self):
        if not self.ui.check_manual_reduction_a.isChecked():
            self.ui.set_piercing_percent_a.setValue(2.00)
            self.ui.set_colib_mm_a.setValue(3.00)
            self.ui.frame_with_reduction_a.setDisabled(True)
        else:
            self.ui.frame_with_reduction_a.setDisabled(False)

    def set_steel(self):
        """This method allows to customise the list of steel grades"""
        dialog_set_steel = SteelSettings(self, self.steels)
        dialog_set_steel.exec_()
        self.refresh()

    def add_steel(self):
        """This method allows to add a new steel to the list of steel grades"""
        dialog_add_steel = AddNewSteel(self, self.steels)
        dialog_add_steel.exec_()
        self.refresh()

    def remove_steel(self):
        """This method allows to remove manually inputted steel from the list of steel grades"""
        current_steel = str(self.ui.choose_steel.currentText())
        if current_steel in self.steels.get_obj_steels():
            self.steels.remove_steel(current_steel)
            self.refresh()

    def remove_steel_a(self):
        """This method allows to remove manually inputted steel from the list of steel grades"""
        current_steel = str(self.ui.choose_steel_a.currentText())
        if current_steel in self.steels.get_obj_steels():
            self.steels.remove_steel(current_steel)
            self.refresh()

    def disable_remove_steel_btn(self):
        """This method disables the remove button if chosen steel grade is not inputted manually"""
        current_steel = str(self.ui.choose_steel.currentText())
        if current_steel in self.steels.get_obj_steels():
            self.ui.discard_steel.setEnabled(True)
        else:
            self.ui.discard_steel.setEnabled(False)

        current_steel = str(self.ui.choose_steel_a.currentText())
        if current_steel in self.steels.get_obj_steels():
            self.ui.discard_steel_a.setEnabled(True)
        else:
            self.ui.discard_steel_a.setEnabled(False)

    def save_excel(self):
        GetExcelFile(self, self.array_with_results, self.arr_parameters, 1)

    def get_excel(self):
        GetExcelFile(self, self.array_with_results, self.arr_parameters, 2)

    def get_and_save_excel(self):
        GetExcelFile(self, self.array_with_results, self.arr_parameters, 3)

    # btn_count click function
    def count_main(self):
        """This method is used when 'Расчет'(Count) button is pressed"""

        # clear StyleSheet border if it was applied
        self.ui.ent_billet_length.setStyleSheet("")
        self.ui.choose_steel.setStyleSheet("")
        self.ui.ent_D1.setStyleSheet("")
        self.ui.ent_Dvp.setStyleSheet("")

        # count for "Штатная" colib_set
        current_colib = str(self.ui.choose_colib.currentText())
        if current_colib == "87/17-01.04":
            colib = "rosniti_first"
        elif current_colib == "П20.28РН":
            colib = "standard_kit_old"
        elif current_colib == "П20.28-ТЗ":
            colib = "standard_kit_new"

        # get values from interface
        f_D1 = (self.ui.ent_D1.currentText())
        f_Doh = self.ui.ent_Doh.currentText()
        if f_Doh.find(",") != -1:
            f_Doh = f_Doh.replace(",", ".")
        f_T = self.ui.ent_T.text()
        f_beta = self.ui.ent_beta.currentText()
        f_Dvp = self.ui.ent_Dvp.text()
        f_nd = self.ui.ent_nd.text()
        key = str(self.ui.choose_steel.currentText())
        billet_length = self.ui.ent_billet_length.text()

        piercing_percent = self.ui.set_piercing_percent.text()
        colib_mm = self.ui.set_colib_mm.text()
        piercing_mm = self.ui.set_piercing_mm.text()

        if self.ui.check_fact.isChecked():
            fact_pc = str(self.ui.get_real_pc.currentText())
            fact_motor_load = int(self.ui.get_real_result.text())
            self.arr_parameters = [
                f_D1, billet_length, f_Doh, f_T, f_beta, f_Dvp, f_nd, key, fact_pc,
                piercing_percent, colib_mm, fact_motor_load, datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"),
                piercing_percent, colib_mm, "Расчет"
            ]
        else:
            self.arr_parameters = [
                f_D1, billet_length, f_Doh, f_T, f_beta, f_Dvp, f_nd, key,
                "null", "null", datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"),
                piercing_percent, colib_mm, "Расчет"
            ]

        if piercing_percent.find(",") != -1:
            piercing_percent = piercing_percent.replace(",", ".")
        if colib_mm.find(",") != -1:
            colib_mm = colib_mm.replace(",", ".")
        if piercing_mm.find(",") != -1:
            piercing_mm = piercing_mm.replace(",", ".")

        # use math_model to get required values
        # [PC_1, PC_2, colib_diameter, forged_billet_length, mu_coeff, reduction_time]
        try:
            arr_results = Model_MLC.math_model(f_D1, billet_length, f_Doh, f_T, f_beta, f_Dvp, f_nd,
                                               key, colib, piercing_percent, colib_mm, self.steels.get_obj_steels())
        except BaseException:
            arr_results = [1111, "Unknown Error!!!"]
        arr_reductions = Model_MLC.get_reductions(
                self.f_D1, self.f_Doh, self.f_T, self.piercing_percent, self.colib_percent,
                piercing_mm, colib_mm
            )

        # show required values in the interface
        if arr_results[0] != 1111 and int(billet_length) > 500 and int(f_Dvp) > 199:
            # 1111 is appended to the array in case of an error
            # the next value in array (index = 1) is the error message

            if arr_results[0] >= 3.52:
                # if the value of PC1 is greater than allowed
                self.ui.get_PC1.setStyleSheet('background-color: rgb(255, 0, 0); '
                                              'color: rgb(255, 255, 255);')
                QtWidgets.QMessageBox.warning(self, "Внимание!", "Превышение максимально "
                                                                   "допустимой токовой нагрузки на PC-1",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            else:
                self.ui.get_PC1.setStyleSheet('background-color: rgb(255, 255, 255); '
                                              'color: rgb(0, 0, 0);')
            if arr_results[1] >= 3.84:
                # if the value of PC2 is greater than allowed
                self.ui.get_PC2.setStyleSheet('background-color: rgb(255, 0, 0); '
                                              'color: rgb(255, 255, 255);')
                QtWidgets.QMessageBox.warning(self, "Внимание!", "Превышение максимально "
                                                                   "допустимой токовой нагрузки на PC-2",
                                              QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            else:
                self.ui.get_PC2.setStyleSheet('background-color: rgb(255, 255, 255); '
                                              'color: rgb(0, 0, 0);')
            # show all three results in the window
            self.ui.get_PC1.setText(str(int(round(arr_results[0] * 1000, 0))))
            self.ui.get_PC2.setText(str(int(round(arr_results[1] * 1000, 0))))
            self.ui.get_colib_diam.setText(str(arr_results[2]))
            self.ui.get_forged_len.setText(str(arr_results[3]))
            self.ui.get_mu.setText(str(arr_results[4]))
            self.ui.get_reduction_time.setText(str(arr_results[5]))
            self.ui.get_piercing_reduction.setText(str(f"{arr_reductions[0]:.2f}"))
            self.ui.get_sum_reduction.setText(str(f"{arr_reductions[1]:.2f}"))
            # change style of lines with results except for pc1 and pc2
            self.ui.get_forged_len.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                 'color: rgb(0, 0, 0);')
            self.ui.get_colib_diam.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                 'color: rgb(0, 0, 0);')
            self.ui.get_mu.setStyleSheet('background-color: rgb(255, 255, 255); '
                                         'color: rgb(0, 0, 0);')
            self.ui.get_reduction_time.setStyleSheet('background-color: rgb(255, 255, 255); '
                                         'color: rgb(0, 0, 0);')
            self.ui.get_piercing_reduction.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                     'color: rgb(0, 0, 0);')
            self.ui.get_sum_reduction.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                     'color: rgb(0, 0, 0);')
            # update the plot with new results
            self.P1f.update_figure(arr_results[0], arr_results[1], arr_results[5])
            # clear array of results property and add new values
            self.array_with_results.clear()
            self.array_with_results.append(current_colib)
            self.array_with_results.append(int(arr_results[0] * 1000))
            self.array_with_results.append(int(arr_results[1] * 1000))
            self.array_with_results.append(int(arr_results[3]))
            self.ui.btn_get_excel.setDisabled(False)
            self.ui.btn_save_excel.setDisabled(False)
            self.ui.btn_get_and_save_excel.setDisabled(False)

            # collect data of usage
            current_data = []
            for item in self.arr_parameters:
                current_data.append(item)
            for item in self.array_with_results:
                current_data.append(item)
            self.existing_data.append(current_data)

            self.ui.check_fact.setChecked(False)

        # in case if the billet length is less then 500 mm
        elif int(billet_length) < 501:
            # error message
            QtWidgets.QMessageBox.warning(self, "Ошибка!", "Слишком маленькая длина заготовки",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.ui.ent_billet_length.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")

        elif int(f_Dvp) < 200:
            # error message
            QtWidgets.QMessageBox.warning(self, "Ошибка!", "Слишком маленький диаметр валков в пережиме",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.ui.ent_Dvp.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")

        # in case of an error
        else:
            # error message
            QtWidgets.QMessageBox.warning(self, "Ошибка!", arr_results[1],
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            if arr_results[1] == "Сталь задана неверно, либо такой стали нет в списке":
                self.ui.choose_steel.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")
            elif arr_results[1] == "Слишком маленький диаметр исходной заготовки":
                self.ui.ent_D1.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")
            elif arr_results[1] == "Возможно, проблемма с диаметром валка в пережиме":
                self.ui.ent_Dvp.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")
            elif arr_results[1] == "Неверный диаметр валков в пережиме":
                self.ui.ent_Dvp.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")

    # btn_analysis click function
    def analyze_main(self):

        # clear StyleSheet border if it was applied
        self.ui.ent_billet_length_a.setStyleSheet("")
        self.ui.choose_steel_a.setStyleSheet("")
        self.ui.ent_D1_a.setStyleSheet("")
        self.ui.ent_Dvp_a.setStyleSheet("")


        """This method is used when 'Анализ'(Analyze) button is pressed"""
        current_colib = str(self.ui.choose_colib_a.currentText())
        if current_colib == "87/17-01.04":
            colib = "rosniti_first"
        elif current_colib == "П20.28РН":
            colib = "standard_kit_old"
        elif current_colib == "П20.28-ТЗ":
            colib = "standard_kit_new"

        # get values from interface
        f_D1 = (self.ui.ent_D1_a.currentText())
        f_Doh = self.ui.ent_Doh_a.currentText()
        if f_Doh.find(",") != -1:
            f_Doh = f_Doh.replace(",", ".")
        f_T = self.ui.ent_T_a.text()
        f_beta = self.ui.ent_beta_a.currentText()
        f_Dvp = self.ui.ent_Dvp_a.text()
        f_nd = self.ui.ent_nd_a.text()
        key = str(self.ui.choose_steel_a.currentText())
        billet_length = self.ui.ent_billet_length_a.text()

        piercing_percent = self.ui.set_piercing_percent_a.text()
        colib_mm = self.ui.set_colib_mm_a.text()

        self.arr_parameters_a = [
            f_D1, billet_length, f_Doh, piercing_percent, colib_mm, f_T, f_beta, f_Dvp, f_nd, key,
            "null", "null", datetime.datetime.now().strftime("%d.%m.%y %H:%M:%S"), "Анализ"
        ]

        if piercing_percent.find(",") != -1:
            piercing_percent = piercing_percent.replace(",", ".")
        if colib_mm.find(",") != -1:
            colib_mm = colib_mm.replace(",", ".")

        # use math_model to analize
        # [[PC1, PC2, value of analized parametr_1], [PC1, PC2, value of analized parametr_n], ...]
        try:
            arr_results = Model_MLC.analysis(self.key_analysis_for, f_D1, billet_length, f_Doh, f_T, f_beta, f_Dvp, f_nd,
                                               key, colib, piercing_percent, colib_mm, self.steels.get_obj_steels())
        except BaseException:
            arr_results = [1111, "Unknown Error!!!"]
        arr_results.reverse()

        print(self.key_analysis_for)
        # show required values in the interface
        if arr_results[0][0] != 1111 and int(billet_length) > 500 and arr_results[1] != 1111 and int(f_Dvp) > 199:
            # show all three results in the window
            if self.key_analysis_for == "forged_chosen" or self.key_analysis_for == "temp_chosen":
                min_pc1 = 10000.0
                min_pc2 = 10000.0
                arr_results.reverse()

                for item in arr_results:
                    min_pc1 = item[2] if item[0] <= 3.52 else min_pc1
                    min_pc2 = item[2] if item[1] <= 3.84 else min_pc2

                self.ui.get_an_pc1.setText(str(int(round(min_pc1, 0))))
                self.ui.get_an_pc2.setText(str(int(round(min_pc2, 0))))

                # change style of lines with results except for pc1 and pc2
                self.ui.get_an_pc1.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                     'color: rgb(0, 0, 0);')
                self.ui.get_an_pc2.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                  'color: rgb(0, 0, 0);')
            else:
                max_pc1 = 10000.0
                max_pc2 = 10000.0

                for item in arr_results:
                    max_pc1 = item[2] if item[0] <= 3.52 else max_pc1
                    max_pc2 = item[2] if item[1] <= 3.84 else max_pc2

                self.ui.get_an_pc1.setText(str(int(round(max_pc1, 0)) if int(round(max_pc1, 0)) != 10000 else "Error"))
                self.ui.get_an_pc2.setText(str(int(round(max_pc2, 0)) if int(round(max_pc2, 0)) != 10000 else "Error"))

                # change style of lines with results except for pc1 and pc2
                self.ui.get_an_pc1.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                  'color: rgb(0, 0, 0);')
                self.ui.get_an_pc2.setStyleSheet('background-color: rgb(255, 255, 255); '
                                                  'color: rgb(0, 0, 0);')

            # update the plot with new results
            self.A1f.update_figure(self.key_analysis_for, arr_results)
            # clear array of results property and add new values
            self.array_with_results.clear()
            self.array_with_results.append(current_colib)

            # collect data of usage
            current_data = []
            for item in self.arr_parameters_a:
                current_data.append(item)
            for item in self.array_with_results:
                current_data.append(item)
            self.existing_data.append(current_data)

        # in case if the billet length is less then 500 mm
        elif int(billet_length) < 501:
            # error message
            QtWidgets.QMessageBox.warning(self, "Ошибка!", "Слишком маленькая длина заготовки",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.ui.ent_billet_length_a.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")

        elif int(f_Dvp) < 200:
            # error message
            QtWidgets.QMessageBox.warning(self, "Ошибка!", "Слишком маленький диаметр валков в пережиме",
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            self.ui.ent_Dvp_a.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")

        # in case of an error
        else:
            # error message
            QtWidgets.QMessageBox.warning(self, "Ошибка", arr_results[0],
                                          QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            if arr_results[0] == "Сталь задана неверно, либо такой стали нет в списке":
                self.ui.choose_steel_a.setStyleSheet("border: 1.5px solid rgb(255, 0, 0);")


def main():
    app = QtWidgets.QApplication(sys.argv)

    pixmap = QtGui.QPixmap(":/images/000.jpg")
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    time.sleep(3)

    # app.setQuitOnLastWindowClosed(False)
    locale = QLocale.system().name()
    translator = QTranslator(app)
    translator.load('{}qtbase_{}.qm'.format(I18N_QT_PATH, locale))
    app.installTranslator(translator)

    window = ProgComp1()
    window.show()

    splash.finish(window)

    app.exec_()


if __name__ == '__main__':
    main()




# https://younglinux.info/oopython/init.php

#### https://python-scripts.com/pyqt5#load-ui-convert-to-py


