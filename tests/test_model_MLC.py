import unittest
from unittest import TestCase

from math_model_v2 import Model_MLC


class TestModel_MLC(unittest.TestCase):
    def test_math_model(self):
        test_model = Model_MLC.math_model(156, 3300, 120, 1100, 14, 485, 111, "32ХГА", "rosniti_first", 2, 3)
        self.assertEqual(test_model[0], 1.87,
                         'PC-1 if args: (156, 3300, 120, 1100, 14, 485, 111, "32ХГА", "rosniti_first") should be 1.87')
        self.assertEqual(test_model[1], 2.35,
                         'PC-2 if args: (156, 3300, 120, 1100, 14, 485, 111, "32ХГА", "rosniti_first") should be 2.35')

    def test_layers(self):
        test_model = Model_MLC.math_model(156, 3300, 120, 1100, 14, 485, 111, "32ХГА", "rosniti_first", 2, 3)
        expected_layers_results = {
            'first_layer': {
                'r_cold_b': 78.0, 'r_hot_b': 79.14114, 'r_before_cog': 77.55831719999999,
                'r_cold_cogged_b': 60.0, 'r_hot_cogged_b': 60.87779999999999,
                'r_after_cog': 62.37779999999999
            },
            'second_layer': {
                'X1': 150.78258210194525, 'X2': 156.47422681496127, 'X3': 203.78525950654978,
                'X4': 219.36429061317926, 'X5': 353.2563052121091
            },
            'third_layer': {
                'D_rf': 150.78258210194525, 'length_after_pitch': 156.47422681496127,
                'X4_plus_length_after_pitch': 203.78525950654978, 'alfa_beta': 219.36429061317926,
                'r_in_p': 353.2563052121091, 'D_in_p': 150.78258210194525, 'unknown_coeff': 156.47422681496127,
                'in_area_length': 203.78525950654978, 'out_area_length': 219.36429061317926
            },
            'fourth_layer': {
                'arr_r_step_i': [75.14521113596986, 67.89534001591937, 63.035366416651016, 60.02532249368921,
                                 60.44385179656195, 61.045181251919466, 61.798073412654844, 62.37779999999999],
                'arr_X_i': [153.29693371807807, 170.4968759744119, 190.72359239084918, 212.91572049539965,
                            235.81574430398788, 258.974801030693, 282.99601408433006, 307.8265979963405],
                'arr_third_of_step': [17.19994225633383, 20.226716416437288, 22.192128104550466,
                                      22.900023808588234, 23.159056726705145, 24.021213053637027,
                                      24.83058391201044, 26.590324465333584],
                'arr_S_i_sec': [18897.598937353177, 16069.71709168215, 14646.527317007587, 14193.767361234393,
                                14035.010766696003, 13531.273786217746, 13090.212121375487, 12223.905388201983],
                'arr_curr_val': [0, 17.19994225633383, 37.42665867277112, 59.61878677732159, 82.51881058590982,
                                 105.67786731261496, 129.699080366252, 154.52966427826243],
                'arr_perim_change': [1.0, 1.0829061715493773, 1.1804018256690436, 1.2200618897429474,
                                     1.1616136103850232, 1.1025041951048158, 1.0411942775776273, 1],
                'arr_sum_third_step': [17.19994225633383, 37.42665867277112, 59.61878677732159,
                                       82.51881058590982, 105.67786731261496, 129.699080366252,
                                       154.52966427826243, 181.11998874359602],

            },
            'fifth_layer': {
                'arr_b_for_Ri': [2202.2743552191596, 2433.6887389059298, 2709.4921610770866, 3014.4173205237544,
                                         3332.5937257475493, 3654.5472396076298, 3988.615489899349],
                'arr_xR_cross_R_ax': [136.94227053813805, 153.53356186501222, 173.307332420192,
                                              195.16899059663857, 217.98069896283442, 241.06320773806056,
                                              265.01428448336446],
                'arr_yR_cross_R_ax': [302.08047884127615, 303.27617215115714, 304.7012188638053,
                                              306.2767344707275, 307.9207178438743, 309.5842171323897,
                                              311.3103119651903]
            },
            'sixth_layer': {
                'arr_D_i_cross_roll': [455.04764909274417, 471.9825851119981, 484.58522614861164, 493.7801305147246,
                                   496.23739508795734, 498.36724423129715, 500.3186975796111],
                'arr_b_fifth': [0, 27.64982047749442, 32.41573299285107, 37.278387772127225, 35.26513701612693,
                            29.984778926054727, 23.363345452756306, 0],
                'arr_whatever': [0, 7.249871120050486, 10.48891630603147, 14.381739106242769, 12.790756597518346,
                             9.167219659062134, 5.504495008520223],
                'arr_eps': [455.04764909274417, 471.9825851119981, 484.58522614861164, 493.7801305147246,
                        496.23739508795734, 498.36724423129715, 500.3186975796111],
                'arr_r_psi': [0, 27.64982047749442, 32.41573299285107, 37.278387772127225, 35.26513701612693,
                          29.984778926054727, 23.363345452756306, 0],
                'arr_deform_eps': [0, 7.249871120050486, 10.48891630603147, 14.381739106242769, 12.790756597518346,
                               9.167219659062134, 5.504495008520223],
                'arr_roll_speed': [455.04764909274417, 471.9825851119981, 484.58522614861164, 493.7801305147246,
                               496.23739508795734, 498.36724423129715, 500.3186975796111],
                'arr_deform_speed': [0, 27.64982047749442, 32.41573299285107, 37.278387772127225, 35.26513701612693,
                                 29.984778926054727, 23.363345452756306, 0],
                'arr_temp_dif': [0, 7.249871120050486, 10.48891630603147, 14.381739106242769, 12.790756597518346,
                             9.167219659062134, 5.504495008520223],
                'arr_bil_temp': [455.04764909274417, 471.9825851119981, 484.58522614861164, 493.7801305147246,
                             496.23739508795734, 498.36724423129715, 500.3186975796111],
                'arr_sig_si': [0, 27.64982047749442, 32.41573299285107, 37.278387772127225, 35.26513701612693,
                           29.984778926054727, 23.363345452756306, 0],
                'arr_unit_roll_press': [0, 7.249871120050486, 10.48891630603147, 14.381739106242769, 12.790756597518346,
                                    9.167219659062134, 5.504495008520223],
                'b_AVG': 23.244650329676332
            },
            'final_layer': {
                'arr_i_pressure': [63778.81932805758, 146432.75059427426, 171601.5507632657, 186612.26769961917,
                                           178740.62330898765, 161649.3062242663, 47563.973916906594],
                'arr_cont_area': [237.78765780545035, 607.4644582205144, 773.3304280752045, 830.6242224049655,
                                          755.5632523588637, 640.7433308576736, 188.53343567132015],
                'whole_roll_press': 956379.2918353772,
                'reach': 26.081882009730133,
                'mom_of_force': 24944.171846199573,
                'Npr': 0.44607443074005715,
                'Ntr': 0.13682277393131187,
                'Ndv': 0.9326355274741903
            },
        }
        for layer in expected_layers_results:
            if test_model[6][layer] == expected_layers_results[layer]:
                self.assertEqual(test_model[6][layer], expected_layers_results[layer])
            else:
                for key in expected_layers_results[layer]:
                    if not isinstance(expected_layers_results[layer][key], list):
                        self.assertEqual(test_model[6][layer][key], expected_layers_results[layer][key],
                                         'wrong variable \"' + key + '\" on \"' + layer + '\"')
                    else:
                        for item in expected_layers_results[layer][key]:
                            step = expected_layers_results[layer][key].index(item)
                            self.assertEqual(test_model[6][layer][key][step], expected_layers_results[layer][key][step],
                                             'wrong variable \"' + key + '\" on step \"' +
                                             str(step) + '\" on \"' + layer + '\"')

    def test_covert_mm_to_percent(self):
        test_model = Model_MLC.covert_mm_to_percent(156, 120, 1100, 2, 3, 'colib_mm_to_percent')
        expected_convert_results = {
            'convert': {
                'r_cold_b': 78.0, 'r_hot_b': 79.14114, 'r_before_cog': 77.55831719999999,
                'r_cold_cogged_b': 60.0, 'r_hot_cogged_b': 60.87779999999999, 'r_after_cog': 62.37779999999999
            },
        }
        for unit in expected_convert_results:
            if test_model[4][unit] == expected_convert_results[unit]:
                self.assertEqual(test_model[4][unit], expected_convert_results[unit])
            else:
                for key in expected_convert_results[unit]:
                    if not isinstance(expected_convert_results[unit][key], list):
                        self.assertEqual(test_model[4][unit][key], expected_convert_results[unit][key],
                                         'wrong variable \"' + key + '\" in \"' + unit + '\"')
                    else:
                        for item in expected_convert_results[unit][key]:
                            step = expected_convert_results[unit][key].index(item)
                            self.assertEqual(test_model[4][unit][key][step], expected_convert_results[unit][key][step],
                                             'wrong variable \"' + key + '\" on step \"' +
                                             str(step) + '\" on \"' + unit + '\"')




if __name__ == '__main__':
    unittest.main()
