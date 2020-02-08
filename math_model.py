import math
import statistics

class Model_MLC:
  calka = {}

  obj_steels_default = {}

  # main math_model
  @staticmethod
  def math_model(D1f, Dohf, Tf, betaf, Dvpf, ndf, key, ob_st=[], cal_out=calka):
    # initial data FROM INTERFACE (change when the interface is ready!!!)

    D1 = int(D1f)  # cold billet diametr
    Doh = int(Dohf)  # cold reduced forging
    T = float(Tf)  # the temperature of the billet
    beta = int(betaf)  # the feed angle
    Dvp = float(Dvpf)  # pitch point roll diametr
    nd = float(ndf)  # shaft speed

    obj_steels = ob_st
    obj_steels_default = Model_MLC.obj_steels_default

    # Steel properties (drop down list)
    k = key
    if k in obj_steels:
      from_ob = obj_steels[k]
    else:
      from_ob = obj_steels_default[k]
    sig0 = from_ob[0]
    steel_a = from_ob[1]
    steel_b = from_ob[2]
    steel_c = from_ob[3]
    # The sector above is to be amended after the interface is ready!!!!!

    if beta < 8 or beta > 14:
      err_txt = 'ОШИБКА!!!\n\nНеверный угол подачи (должен быть в диапазоне 8 - 14)'
      print(err_txt)
      err_uin = 1111
      arr_err = []
      arr_err.append(err_uin)
      arr_err.append(err_txt)
      return arr_err
    if D1 == 0 or Doh == 0 or T == 0 or Dvp == 0 or nd == 0 or sig0 == 0 or \
            steel_a == 0 or steel_b == 0 or steel_c == 0:
      err_txt = 'ОШИБКА!!!\n\nВходные данные не могут быть равны 0'
      print(err_txt)
      err_uin = 1111
      arr_err = []
      arr_err.append(err_uin)
      arr_err.append(err_txt)
      return arr_err



