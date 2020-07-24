import xlrd
from math_model_v2 import Model_MLC


# def get_colib_from_excel_2():
#   """This method allows to get the colib data from outer .xlsx file"""
#   calka = {}
#   wb = xlrd.open_workbook('добавление новой калибровки/for_Dict_1_new_colib.xlsx')
#   sh = wb.sheet_by_index(0)
#   n = 2
#
#   # Add all for a
#   for ind_colib_prop in range(1, 4):  # layer for properties (a, b, c)
#     # choose property
#     if ind_colib_prop == 1:
#       colib_prop = '_a'
#     elif ind_colib_prop == 2:
#       colib_prop = '_b'
#     elif ind_colib_prop == 3:
#       colib_prop = '_c'
#     # choose "beta" angle
#     for n in range(2, 41):
#       if n < 7:
#         beta = 14
#       elif n < 12:
#         beta = 13
#       elif n < 17:
#         beta = 12
#       elif n < 22:
#         beta = 11
#       elif n < 27:
#         beta = 10
#       elif n < 32:
#         beta = 9
#       elif n < 37:
#         beta = 8
#       elif n < 41:
#         beta = 7
#       # add all property's values to the dict {calka}
#       for i in range(n, n + 3):
#         if str(sh.cell(n, 0).value) == '':
#           continue
#         key_name = str(sh.cell(n, 0).value) + str(beta) + colib_prop
#         key_value = sh.cell(n, ind_colib_prop).value
#         calka[key_name] = float(key_value)
#         i += 1
#
#       n += 7
#     ind_colib_prop += 1
#   print(calka)
#   return calka

def get_colib_from_excel_2():
    """This method allows to get the colib data from outer .xlsx file"""
    calka = {}
    # wb = xlrd.open_workbook('for_Dict_2.xlsx')
    wb = xlrd.open_workbook('добавление новой калибровки/for_Dict_1_standard_colib_new.xlsx')
    # wb = xlrd.open_workbook('добавление новой калибровки/for_Dict_1.xlsx')
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

x = get_colib_from_excel_2()

print(Model_MLC.colibs["rosniti_first"] == x)
