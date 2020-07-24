import math
import statistics

class Model_MLC:
  calka = {'in1_14_a': 0.00020132, 'crest_14_a': 0.0, 'in2_14_a': 0.00011999, 'pinch_14_a': 0.00011784,
           'out1_14_a': 0.00011398, 'out2_14_a': 0.00012267,
           'in1_13_a': 0.00017331, 'crest_13_a': 0.0, 'in2_13_a': 0.0001037, 'pinch_13_a': 0.00010188,
           'out1_13_a': 9.827e-05, 'out2_13_a': 0.00010531,
           'in1_12_a': 0.00014747, 'crest_12_a': 0.0, 'in2_12_a': 8.855e-05, 'pinch_12_a': 8.698e-05,
           'out1_12_a': 8.373e-05, 'out2_12_a': 8.938e-05,
           'in1_11_a': 0.00012376, 'crest_11_a': 0.0, 'in2_11_a': 7.454e-05, 'pinch_11_a': 7.321e-05,
           'out1_11_a': 7.035e-05, 'out2_11_a': 7.484e-05,
           'in1_10_a': 0.00010217, 'crest_10_a': 0.0, 'in2_10_a': 6.169e-05, 'pinch_10_a': 6.063e-05,
           'out1_10_a': 5.814e-05, 'out2_10_a': 6.165e-05,
           'in1_9_a': 8.268e-05, 'crest_9_a': 0.0, 'in2_9_a': 9.651e-05, 'pinch_9_a': 4.92e-05,
           'out1_9_a': 4.709e-05, 'out2_9_a': 4.978e-05,
           'in1_8_a': 6.527e-05, 'crest_8_a': 0.0, 'in2_8_a': 3.962e-05, 'pinch_8_a': 3.894e-05,
           'out1_8_a': 3.721e-05, 'out2_8_a': 3.924e-05,
           'in1_7_a': 4.993e-05, 'crest_7_a': 0.0, 'in2_7_a': 3.038e-05, 'pinch_7_a': 2.986e-05,
           'out1_7_a': 2.849e-05, 'out2_7_a': 2.997e-05,
           'in1_14_b': -0.30469483, 'crest_14_b': -1.20321048, 'in2_14_b': -0.28361781, 'pinch_14_b': -0.040761,
           'out1_14_b': -0.03043103, 'out2_14_b': 0.02375363,
           'in1_13_b': -0.29680594, 'crest_13_b': -1.20754747, 'in2_13_b': -0.27881288, 'pinch_13_b': -0.03508259,
           'out1_13_b': -0.0248454, 'out2_13_b': 0.03062524,
           'in1_12_b': -0.2895794, 'crest_12_b': -1.21157099, 'in2_12_b': -0.27438535, 'pinch_12_b': -0.02982633,
           'out1_12_b': -0.01972938, 'out2_12_b': 0.03683477,
           'in1_11_b': -0.28299565, 'crest_11_b': -1.21527939, 'in2_11_b': -0.27033017, 'pinch_11_b': -0.02500719,
           'out1_11_b': -0.01506939, 'out2_11_b': 0.04242044,
           'in1_10_b': -0.27703737, 'crest_10_b': -1.21867146, 'in2_10_b': -0.26664007, 'pinch_10_b': -0.02063649,
           'out1_10_b': -0.01085341, 'out2_10_b': 0.04741744,
           'in1_9_b': -0.27168926, 'crest_9_b': -1.22174791, 'in2_9_b': -0.28042107, 'pinch_9_b': -0.01669203,
           'out1_9_b': -0.00707036, 'out2_9_b': 0.05186181,
           'in1_8_b': -0.26693785, 'crest_8_b': -1.22449833, 'in2_8_b': -0.26037202, 'pinch_8_b': -0.01317696,
           'out1_8_b': -0.00371068, 'out2_8_b': 0.05576569,
           'in1_7_b': -0.26277156, 'crest_7_b': -1.22693111, 'in2_7_b': -0.25777269, 'pinch_7_b': -0.01007906,
           'out1_7_b': -0.00076586, 'out2_7_b': 0.059163,
           'in1_14_c': 59.58709859, 'crest_14_c': 199.64469648, 'in2_14_c': 52.81428726, 'pinch_14_c': 3.41293534,
           'out1_14_c': 1.33265467, 'out2_14_c': -18.89284337,
           'in1_13_c': 58.86734397, 'crest_13_c': 199.47980655, 'in2_13_c': 52.29731902, 'pinch_13_c': 2.92426085,
           'out1_13_c': 0.86055106, 'out2_13_c': -19.52331881,
           'in1_12_c': 58.21143587, 'crest_12_c': 199.32912074, 'in2_12_c': 51.82458079, 'pinch_12_c': 2.47544094,
           'out1_12_c': 0.433206, 'out2_12_c': -20.08008645,
           'in1_11_c': 57.61674221, 'crest_11_c': 199.1921704, 'in2_11_c': 51.39462134, 'pinch_11_c': 2.06720254,
           'out1_11_c': 0.04819452, 'out2_11_c': -20.57007582,
           'in1_10_c': 57.08092763, 'crest_10_c': 199.0685885, 'in2_10_c': 51.00592748, 'pinch_10_c': 1.69993345,
           'out1_10_c': -0.29661852, 'out2_10_c': -20.99955743,
           'in1_9_c': 56.60192816, 'crest_9_c': 198.95831217, 'in2_9_c': 52.22222666, 'pinch_9_c': 1.37064379,
           'out1_9_c': -0.60317692, 'out2_9_c': -21.37490177,
           'in1_8_c': 56.17792904, 'crest_8_c': 198.85965393, 'in2_8_c': 50.35060386, 'pinch_8_c': 1.07904149,
           'out1_8_c': -0.87315017, 'out2_8_c': -21.69821799,
           'in1_7_c': 55.80735234, 'crest_7_c': 198.77373799, 'in2_7_c': 50.08085344, 'pinch_7_c': 0.82333169,
           'out1_7_c': -1.1080165, 'out2_7_c': -21.97542971}

  obj_steels_default = {'32ХГА': [92.4, 0.134, 0.25, 3.34], '10': [87.6, 0.125, 0.266, 2.46],
                        '15Г': [103, 0.126, 0.188, 2.74], '23Г2А': [88.2, 0.123, 0.229, 3.23],
                        '35ГС': [89.6, 0.136, 0.187, 2.79], 'А35Г2': [83.5, 0.151, 0.122, 3.66],
                        '30ХГСА': [92.4, 0.134, 0.250, 3.34], '15ХСНД': [93.2, 0.122, 0.226, 2.90],
                        '20ХГ2С': [95.8, 0.125, 0.213, 3.65], '30ХГСНА': [97.6, 0.116, 0.140, 3.42],
                        '15ХГНТА': [108, 0.108, 0.257, 3.25], '45': [87.4, 0.143, 0.173, 3.05],
                        '40Х': [87.5, 0.130, 0.170, 3.62], '40ХГНМ': [103, 0.173, 0.144, 2.64],
                        '38ХМЮА': [100, 0.114, 0.273, 3.72], '40Х13': [76.160, 0.103, 0.2932, 3.758],
                        '40ХН2МА': [92.7, 0.125, 0.175, 3.40], '20ХГСНМ': [81.1, 0.085, 0.253, 3.80],
                        '12Х2Н4А': [104, 0.100, 0.226, 3.20], '15Х13': [145, 0.102, 0.125, 3.50],
                        '20Х13': [136, 0.132, 0.210, 3.26], '12Х18Н10Т': [222, 0.112, 0.088, 4.35],
                        '35': [76.624, 0.138, 0.1913, 2.981], '40': [76.946, 0.140, 0.1942, 2.993],
                        '20к': [76.733, 0.140, 0.1637, 3.467], '09Г2': [85.131, 0.133, 0.1717, 3.572],
                        '09Г2С': [84.246, 0.127, 0.1776, 3.511], '10Г2С1': [83.528, 0.127, 0.1795, 3.513],
                        '10Г2ФБ': [107.671, 0.118, 0.1797, 4.077], '12ГС': [80.646, 0.128, 0.1707, 3.451],
                        '13Г1СУ': [87.463, 0.134, 0.1939, 3.761], '14Г2': [83.842, 0.135, 0.1730, 3.563],
                        '14ХГС': [85.765, 0.129, 0.1753, 3.523], '16ГФБ': [89.912, 0.122, 0.1811, 3.110],
                        '17Г1С': [83.647, 0.132, 0.1805, 3.530], '17ГС': [82.393, 0.132, 0.1776, 3.507],
                        '35Г2': [81.881, 0.146, 0.1916, 3.603], '35ХГСА': [90.385, 0.140, 0.2016, 3.679],
                        '40Г': [75.235, 0.140, 0.1955, 3.023], '40Г2': [82.194, 0.148, 0.1945, 3.614],
                        '40ХН': [88.393, 0.146, 0.1890, 3.517], '45Г2': [82.547, 0.150, 0.1970, 3.625],
                        '45ХН': [73.298, 0.148, 0.1914, 3.527], '50ХФА': [81.458, 0.128, 0.1654, 3.351],
                        '08Х17Т': [81.417, 0.066, 0.2596, 4.316], '30Х13': [82.993, 0.147, 0.1879, 3.619]}

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

    PC1 = D1 / 40
    PC2 = D1 / 30

    arr_math_model = []
    arr_math_model.append(PC1)
    arr_math_model.append(PC2)
    return arr_math_model



  @staticmethod
  def covert_mm_to_percent(D1f, Dohf, Tf, piercing_convertf, colib_convertf, key):
    # dict for testing
    test_dict = {}
    arr_covert_results = []

    D1 = int(D1f)  # cold billet diameter
    Doh = float(Dohf)  # cold reduced forging
    T = float(Tf)  # the temperature of the billet
    piercing_convert = float(piercing_convertf)
    colib_convert = float(colib_convertf)


    r_cold_b = D1 / 2  # Cold billet radius
    r_hot_b = r_cold_b * (1 + 0.0000133 * T)  # Hot billet radius
    r_before_cog = r_hot_b * (1 - (piercing_convert / 100))  # billet radius before cogging mill
    r_cold_cogged_b = Doh / 2  # biller radius after cogging mill
    r_hot_cogged_b = r_cold_cogged_b * (1 + 0.0000133 * T)
    r_after_cog = r_hot_cogged_b + colib_convert / 2

    test_convert = {
        'r_cold_b': r_cold_b,
        'r_hot_b': r_hot_b,
        'r_before_cog': r_before_cog,
        'r_cold_cogged_b': r_cold_cogged_b,
        'r_hot_cogged_b': r_hot_cogged_b,
        'r_after_cog': r_after_cog,
    }
    test_dict['convert'] = test_convert

    if key == 'piercing_percent_to_mm':
        convert_piercing_percent_to_mm = r_hot_b - r_before_cog
    if key == 'piercing_mm_to_percent':
        r_before_cog = r_hot_b - piercing_convert / 2
        convert_piercing_mm_to_percent = 100 - r_before_cog * 100 / r_hot_b
    if key == 'colib_percent_to_mm':
        convert_colib_mm_to_percent = r_after_cog * 100 / r_hot_cogged_b - 100
    if key == 'colib_mm_to_percent':
        r_after_cog = r_hot_cogged_b + colib_convert / 2
        convert_colib_percent_to_mm = r_after_cog * 100 / r_hot_cogged_b - 100

    arr_covert_results.append(convert_piercing_percent_to_mm if 'convert_piercing_percent_to_mm' in locals() else 0)
    arr_covert_results.append(convert_piercing_mm_to_percent if 'convert_piercing_mm_to_percent' in locals() else 0)
    arr_covert_results.append(convert_colib_mm_to_percent if 'convert_colib_mm_to_percent' in locals() else 0)
    arr_covert_results.append(convert_colib_percent_to_mm if 'convert_colib_percent_to_mm' in locals() else 0)
    arr_covert_results.append(test_dict)

    return arr_covert_results

  @staticmethod
  def get_reductions(D1f, Dohf, Tf, piercing_percentf, colib_convertf, colib_mmf, piercing_mmf):
    # dict for testing
    test_dict = {}
    arr_covert_results = []

    D1 = int(D1f)  # cold billet diameter
    Doh = float(Dohf)  # cold reduced forging
    T = float(Tf)  # the temperature of the billet
    piercing_percent = float(piercing_percentf)
    colib_convert = float(colib_convertf)
    colib_mm = float(colib_mmf)
    piercing_mm = float(piercing_mmf)

    r_cold_b = D1 / 2  # Cold billet radius
    r_hot_b = r_cold_b * (1 + 0.0000133 * T)  # Hot billet radius
    r_before_cog = r_hot_b * (1 - (piercing_percent / 100))  # billet radius before cogging mill
    r_cold_cogged_b = Doh / 2  # biller radius after cogging mill
    r_hot_cogged_b = r_cold_cogged_b * (1 + 0.0000133 * T)
    r_after_cog = r_hot_cogged_b + colib_mm

    test_convert = {
        'r_cold_b': r_cold_b,
        'r_hot_b': r_hot_b,
        'r_before_cog': r_before_cog,
        'r_cold_cogged_b': r_cold_cogged_b,
        'r_hot_cogged_b': r_hot_cogged_b,
        'r_after_cog': r_after_cog,
    }
    test_dict['convert'] = test_convert

    piercing_reduction = ((r_hot_b * 2 - piercing_mm) - (r_after_cog * 2 + colib_mm)) * 100 / (r_hot_b * 2 - piercing_mm)
    sum_reduction = ((r_hot_b * 2) - (r_after_cog * 2)) * 100 / (r_hot_b * 2)

    arr_covert_results.append(piercing_reduction)
    arr_covert_results.append(sum_reduction)

    arr_covert_results.append(test_dict)

    return arr_covert_results

