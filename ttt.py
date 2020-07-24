# import xlwt
#
#
# wb = xlwt.Workbook()
# sh = wb.add_sheet('report')
# sh.write(0, 1, "Date:")
# print('qqq')
# # sh.write(0, 0, 111)
# try:
#   wb.save('output.xls')
# except PermissionError:
#   print("Sorry")
# #
# import datetime
#
# now = datetime.datetime.now()
#
#
# print ("Текущая дата и время с использованием метода str:")
# print (now.strftime("%d-%m-%Y %H:%M"))

#
# import xlwt
#
# styles = dict(
#     bold = 'font: bold 1',
#     italic = 'font: italic 1',
#     # Wrap text in the cell
#     wrap_bold = 'font: bold 1; align: wrap 1;',
#     # White text on a blue background
#     reversed = 'pattern: pattern solid, fore_color blue; font: color white;',
#     # Light orange checkered background
#     light_orange_bg = 'pattern: pattern fine_dots, fore_color white, back_color orange;',
#     # Heavy borders
#     bordered = 'border: top thick, right thick, bottom thick, left thick;',
#     # 16 pt red text
#     big_red = 'font: height 320, color red;',
# )
#
# book = xlwt.Workbook()
# sheet = book.add_sheet('Style demo')
#
# print(sorted(styles))
# print(styles['bold'])
#
# for idx, k in enumerate(sorted(styles)):
#     style = xlwt.easyxf(styles[k])
#     sheet.write(idx, 0, k)
#     sheet.write(idx, 1, styles[k], style)
#
# book.save('Example.xls')
#
# import os
# import wx
# from wx.html import HtmlEasyPrinting, HtmlWindow
#
#
# class SnapshotPrinter(wx.Frame):
#     def __init__(self, title='Snapshot Printer'):
#         wx.Frame.__init__(self, None, title=title, size=(650, 400))
#
#         self.panel = wx.Panel(self)
#         self.printer = HtmlEasyPrinting(
#             name='Printing', parentWindow=None)
#
#         self.html = HtmlWindow(self.panel)
#         self.html.SetRelatedFrame(self, self.GetTitle())
#
#         if not os.path.exists('screenshot.htm'):
#             self.createHtml()
#
#         self.html.LoadPage('screenshot.htm')
#
#         pageSetupBtn = wx.Button(self.panel, label='Page Setup')
#         printBtn = wx.Button(self.panel, label='Print')
#         cancelBtn = wx.Button(self.panel, label='Cancel')
#
#         self.Bind(wx.EVT_BUTTON, self.onSetup, pageSetupBtn)
#         self.Bind(wx.EVT_BUTTON, self.onPrint, printBtn)
#         self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)
#
#         sizer = wx.BoxSizer(wx.VERTICAL)
#         btnSizer = wx.BoxSizer(wx.HORIZONTAL)
#         sizer.Add(self.html, 1, wx.GROW)
#         btnSizer.Add(pageSetupBtn, 0, wx.ALL, 5)
#         btnSizer.Add(printBtn, 0, wx.ALL, 5)
#         btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
#         sizer.Add(btnSizer)
#
#         self.panel.SetSizer(sizer)
#         self.panel.SetAutoLayout(True)
#
#     def createHtml(self):
#         '''
#         Creates an html file in the home directory of the application
#         that contains the information to display the snapshot
#         '''
#         print('creating html...')
#
#         html = '''<html>\n<body>\n<center>
#                 <img src=myImage.png width=516 height=314>
#                 </center>\n</body>\n</html>'''
#
#         with open('screenshot.htm', 'w') as fobj:
#             fobj.write(html)
#
#     def onSetup(self, event):
#         self.printer.PageSetup()
#
#     def onPrint(self, event):
#         self.sendToPrinter()
#
#     def sendToPrinter(self):
#         self.printer.GetPrintData().SetPaperId(wx.PAPER_LETTER)
#         self.printer.PrintFile(self.html.GetOpenedPage())
#
#     def onCancel(self, event):
#         self.Close()
#
#
# if __name__ == '__main__':
#     app = wx.App(False)
#     frame = SnapshotPrinter()
#     frame.Show()
#     app.MainLoop()
#
#

from PyQt5 import QtChart, QtCore, QtGui, QtPrintSupport, QtWidgets
import sys
import random

# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         QtWidgets.QWidget.__init__(self)
#         self.setWindowTitle(self.tr('Chart Printing'))
#         self.chart = QtChart.QChart()
#         self.chart_view = QtChart.QChartView(self.chart)
#         self.chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
#         self.buttonPreview = QtWidgets.QPushButton('Preview', self)
#         self.buttonPreview.clicked.connect(self.handle_preview)
#         self.buttonPrint = QtWidgets.QPushButton('Print', self)
#         self.buttonPrint.clicked.connect(self.handle_print)
#         layout = QtWidgets.QGridLayout(self)
#         layout.addWidget(self.chart_view, 0, 0, 1, 2)
#         layout.addWidget(self.buttonPreview, 1, 0)
#         layout.addWidget(self.buttonPrint, 1, 1)
#         self.create_chart()
#
#     def create_chart(self):
#         self.chart.setTitle("Chart Print Preview and Print Example")
#         for i in range(5):
#             series = QtChart.QLineSeries()
#             series.setName("Line {}".format(i + 1))
#             series.append(0, 0)
#             for i in range(1, 10):
#                 series.append(i, random.randint(1, 9))
#             series.append(10, 10)
#             self.chart.addSeries(series)
#         self.chart.createDefaultAxes()
#
#     def handle_print(self):
#         printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
#         dialog = QtPrintSupport.QPrintDialog(printer, self)
#         if dialog.exec_() == QtPrintSupport.QPrintDialog.Accepted:
#             self.handle_paint_request(printer)
#
#     def handle_preview(self):
#         dialog = QtPrintSupport.QPrintPreviewDialog()
#         dialog.paintRequested.connect(self.handle_paint_request)
#         dialog.exec_()
#
#     def handle_paint_request(self, printer):
#         painter = QtGui.QPainter(printer)
#         painter.setViewport(self.chart_view.rect())
#         painter.setWindow(self.chart_view.rect())
#         self.chart_view.render(painter)
#         painter.end()
#
# if __name__ == '__main__':
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.resize(640, 480)
#     window.show()
#     sys.exit(app.exec_())
#
# x = {
#     "q": 1,
#     "w":1.6,
#     "e":3,
# }
#
# y = {
#     "q": 1,
#     "w":1.5,
#     "e":3,
# }
#
# print(x == y)
# import os
# import subprocess
# user_path = os.path.expanduser("~")
# data_file = os.path.join(user_path, "data_log.bbld")
# subprocess.call(['attrib', '-h', data_file])
# f = open(data_file, "r")
# existing_data = f.read()
# print(existing_data)
#
# f.close()
# subprocess.call(['attrib', '+h', data_file])

# x = eval("[[['156'], [3600.0], ['120'], ['1160'], ['14'], ['485'], ['200'], ['32ХГА'], ['Роснити'], [2.06], [1.87], [6084.0]]]")
# y = [['156'], [3600.0], ['120'], ['1160'], ['14'], ['485'], ['200'], ['32ХГА'], ['Роснити'], [2.06], [1.87], [6084.0]]
#
# x.append(y)
# print(x[1][2])


# q = [[['156'], [3600.0], ['120'], ['1160'], ['14'], ['485'], ['200'], ['32ХГА'], ['Роснити'], [2.06], [1.87], [6084.0]]][[['156'], [3600.0], ['120'], ['1160'], ['14'], ['485'], ['200'], ['32ХГА'], ['Роснити'], [2.06], [1.87], [6084.0]], [['156'], [3600.0], ['120'], ['1160'], ['14'], ['485'], ['200'], ['32ХГА'], ['Роснити'], [2.06], [1.87], [6084.0]]]



# import base64
# x = [['156', 3600.0, '120', '1160', '14', '485', '200', '32ХГА', 'null', 'null', 'Роснити', 3110, 3890, 6084], ['156', 3600.0, '120', '1160', '14', '485', '200', '32ХГА', 'null', 'null', 'П20.28РН', 2730, 2480, 6084], ['156', 3600.0, '120', '1160', '14', '485', '200', '32ХГА', 'null', 'null', 'П20.28-ТЗ', 2680, 2440, 6084]]
# d = base64.b64encode(str.encode(str(x)))
# print(d)
# e = base64.b64decode(d).decode()
# print(eval(e)[1])

# x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#
# for item in x:
#     if item % 2 == 0:
#         print(item)
#     else:
#         continue

# x = [[11.67, 14.62, 36], [11.32, 14.19, 37], [10.99, 13.77, 38], [10.68, 13.37, 39], [10.39, 13.0, 40], [10.12, 12.67, 41], [9.85, 12.33, 42], [9.6, 12.02, 43], [9.36, 11.71, 44], [9.14, 11.44, 45], [8.92, 11.17, 46], [8.71, 10.9, 47], [8.52, 10.67, 48], [8.32, 10.42, 49], [8.14, 10.19, 50], [7.96, 9.96, 51], [7.81, 9.78, 52], [7.64, 9.57, 53], [7.47, 9.36, 54], [7.34, 9.19, 55], [7.19, 9.01, 56], [7.05, 8.82, 57], [6.92, 8.65, 58], [6.78, 8.49, 59], [6.66, 8.34, 60], [6.54, 8.17, 61], [6.4, 8.03, 62], [6.28, 7.86, 63], [6.18, 7.74, 64], [6.06, 7.59, 65], [5.95, 7.45, 66], [5.83, 7.3, 67], [5.74, 7.2, 68], [5.65, 7.07, 69], [5.53, 6.93, 70], [5.44, 6.8, 71], [5.33, 6.68, 72], [5.27, 6.59, 73], [5.16, 6.47, 74], [5.06, 6.34, 75], [5.0, 6.26, 76], [4.89, 6.12, 77], [4.82, 6.03, 78], [4.74, 5.93, 79], [4.64, 5.8, 80], [4.56, 5.7, 81], [4.48, 5.62, 82], [4.39, 5.51, 83], [4.32, 5.41, 84], [4.24, 5.3, 85], [4.17, 5.2, 86], [4.12, 5.16, 87], [4.05, 5.05, 88], [3.96, 4.95, 89], [3.87, 4.85, 90], [3.82, 4.78, 91], [3.76, 4.7, 92], [3.65, 4.58, 93], [3.62, 4.53, 94], [3.53, 4.41, 95], [3.49, 4.37, 96], [3.4, 4.26, 97], [3.35, 4.2, 98], [3.26, 4.1, 99], [3.23, 4.06, 100], [3.13, 3.91, 101], [3.1, 3.87, 102], [2.99, 3.74, 103], [2.96, 3.7, 104], [2.91, 3.64, 105], [2.81, 3.52, 106], [2.78, 3.47, 107], [2.75, 3.43, 108], [2.64, 3.31, 109], [2.6, 3.27, 110], [2.57, 3.2, 111], [2.45, 3.06, 112], [2.42, 3.02, 113], [2.42, 3.02, 114], [2.37, 2.97, 115], [2.25, 2.83, 116], [2.22, 2.77, 117], [2.17, 2.72, 118], [2.14, 2.68, 119], [2.01, 2.52, 120], [1.92, 2.41, 121], [1.83, 2.29, 122], [1.72, 2.14, 123], [1.66, 2.08, 124], [1.54, 1.91, 125], [1.49, 1.87, 126], [1.45, 1.81, 127], [1.39, 1.75, 128], [1.34, 1.66, 129], [1.28, 1.6, 130], [1.22, 1.54, 131], [1.1, 1.37, 132], [1.06, 1.33, 133], [1.03, 1.27, 134], [0.98, 1.23, 135], [0.91, 1.12, 136], [0.83, 1.04, 137], [0.76, 0.94, 138], [0.68, 0.85, 139], [0.6, 0.75, 140], [0.5, 0.62, 141], [0.42, 0.54, 142], [0.35, 0.44, 143], [0.27, 0.33, 144], [0.17, 0.21, 145], [0.24, 0.29, 146]]
# y = [[11.67, 14.62, 36], [11.32, 14.19, 37], [10.99, 13.77, 38], [10.68, 13.37, 39], [10.39, 13.0, 40], [10.12, 12.67, 41], [9.85, 12.33, 42], [9.6, 12.02, 43], [9.36, 11.71, 44], [9.14, 11.44, 45], [8.92, 11.17, 46], [8.71, 10.9, 47], [8.52, 10.67, 48], [8.32, 10.42, 49], [8.14, 10.19, 50], [7.96, 9.96, 51], [7.81, 9.78, 52], [7.64, 9.57, 53], [7.47, 9.36, 54], [7.34, 9.19, 55], [7.19, 9.01, 56], [7.05, 8.82, 57], [6.92, 8.65, 58], [6.78, 8.49, 59], [6.66, 8.34, 60], [6.54, 8.17, 61], [6.4, 8.03, 62], [6.28, 7.86, 63], [6.18, 7.74, 64], [6.06, 7.59, 65], [5.95, 7.45, 66], [5.83, 7.3, 67], [5.74, 7.2, 68], [5.65, 7.07, 69], [5.53, 6.93, 70], [5.44, 6.8, 71], [5.33, 6.68, 72], [5.27, 6.59, 73], [5.16, 6.47, 74], [5.06, 6.34, 75], [5.0, 6.26, 76], [4.89, 6.12, 77], [4.82, 6.03, 78], [4.74, 5.93, 79], [4.64, 5.8, 80], [4.56, 5.7, 81], [4.48, 5.62, 82], [4.39, 5.51, 83], [4.32, 5.41, 84], [4.24, 5.3, 85], [4.17, 5.2, 86], [4.12, 5.16, 87], [4.05, 5.05, 88], [3.96, 4.95, 89], [3.87, 4.85, 90], [3.82, 4.78, 91], [3.76, 4.7, 92], [3.65, 4.58, 93], [3.62, 4.53, 94], [3.53, 4.41, 95], [3.49, 4.37, 96], [3.4, 4.26, 97], [3.35, 4.2, 98], [3.26, 4.1, 99], [3.23, 4.06, 100], [3.13, 3.91, 101], [3.1, 3.87, 102], [2.99, 3.74, 103], [2.96, 3.7, 104], [2.91, 3.64, 105], [2.81, 3.52, 106], [2.78, 3.47, 107], [2.75, 3.43, 108], [2.64, 3.31, 109], [2.6, 3.27, 110], [2.57, 3.2, 111], [2.45, 3.06, 112], [2.42, 3.02, 113], [2.42, 3.02, 114], [2.37, 2.97, 115], [2.25, 2.83, 116], [2.22, 2.77, 117], [2.17, 2.72, 118], [2.14, 2.68, 119], [2.01, 2.52, 120], [1.92, 2.41, 121], [1.83, 2.29, 122], [1.72, 2.14, 123], [1.66, 2.08, 124], [1.54, 1.91, 125], [1.49, 1.87, 126], [1.45, 1.81, 127], [1.39, 1.75, 128], [1.34, 1.66, 129], [1.28, 1.6, 130], [1.22, 1.54, 131], [1.1, 1.37, 132], [1.06, 1.33, 133], [1.03, 1.27, 134], [0.98, 1.23, 135], [0.91, 1.12, 136], [0.83, 1.04, 137], [0.76, 0.94, 138], [0.68, 0.85, 139], [0.6, 0.75, 140], [0.5, 0.62, 141], [0.42, 0.54, 142], [0.35, 0.44, 143], [0.27, 0.33, 144], [0.17, 0.21, 145], [0.24, 0.29, 146]]
#
# print(x == y)
#
#

x = 0

print(x ** 0.5)







