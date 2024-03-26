import math
import numpy as np
from scipy.stats import f


class Gage:
    def __init__(self, data, LSL, USL):
        self.data = data
        self.USL = USL
        self.LSL = LSL
        self.range_spec = self.USL - self.LSL

    def grr_contribution(self, *args):
        # -------------- Gage contribution --------------
        try:
            # grr_result_lst.append(args)
            grr_STD_result_lst = np.array(args[0])
            grr_percent_study_var = grr_STD_result_lst / grr_STD_result_lst[4] * 100
            # total_GageRR = (varComp_reproducibility ** 2 + varComp_Repeatability ** 2) ** (1 / 2)
        except ZeroDivisionError as exz:
            raise exz.args
        except Exception as ex:
            print(" -------------- Gage Evaluation -------------- \r\n" + str(ex.args))
            raise ex.args

    def grr_evaluation(self, *args):
        # -------------- Gage Evaluation --------------
        try:
            grr_STD_result_lst = np.array(args[0])
            grr_percent_study_var = grr_STD_result_lst / grr_STD_result_lst[4] * 100
            grr_tolerance = grr_STD_result_lst / self.range_spec * 100
            # total_GageRR = (varComp_reproducibility ** 2 + varComp_Repeatability ** 2) ** (1 / 2)
        except ZeroDivisionError as exz:
            raise exz.args
        except Exception as ex:
            print(" -------------- Gage Evaluation -------------- \r\n" + str(ex.args))
            raise ex.args

    def grr_variance(self, *args):
        # -------------- GRR_Variance --------------
        # range_spec = self
        range_spec, grr_shape1, grr_shape2, MS_0, MS_1, MS_2, MS_3, MS_0_t2, MS_1_t2, MS_2_t2, p_value1, p_value3, F3 = args
        try:
            # if MS_0_t2 == np.none:
            #     pass
            if p_value3 >= 0.05:
                varComp_op = (MS_1_t2 - MS_2_t2) / (grr_shape1 * grr_shape2) if MS_1_t2 > MS_2_t2 else 0
                varComp_op_dut = 0
                varComp_Repeatability = MS_2_t2
                varComp_part_to_part = (MS_0_t2 - MS_2_t2) / (3 * 3) if MS_0_t2 > MS_1_t2 else 0  # ???????
                varComp_reproducibility = varComp_op
            else:
                varComp_op = (MS_1 - MS_2) / (grr_shape1 * grr_shape2) if MS_1 > MS_2 else 0
                varComp_op_dut = (MS_2 - MS_3) / grr_shape2
                varComp_Repeatability = MS_3
                varComp_part_to_part = (MS_0 - MS_2) / (3 * 3) if MS_0 > MS_3 else 0  # ???????
                varComp_reproducibility = varComp_op + varComp_op_dut
            varComp_total_RageRR = varComp_reproducibility + varComp_Repeatability
            varComp_total_variation = varComp_total_RageRR + varComp_part_to_part
            # grr_op = varComp_op ** (1/2)
            # grr_op_dut = varComp_op_dut ** (1/2)
            reproducibility = varComp_op ** (1 / 2) if p_value3 >= 0.05 else (varComp_op + varComp_op_dut) ** (1 / 2)
            total_RageRR = (reproducibility ** 2 + varComp_Repeatability) ** (1 / 2)
            total_variation = (total_RageRR ** 2 + varComp_part_to_part) ** (1 / 2)
            grr_tolerance = total_RageRR * 6 / range_spec * 100

            # print("varComp_op: ", varComp_op)
            # print("varComp_op_dut: ", varComp_op_dut)
            # print("varComp_part_to_part: ", varComp_part_to_part)
            # print("varComp_op: ", varComp_op)
            # print("varComp_op_dut: ", varComp_op_dut)
            # print("varComp_Repeatability: ", varComp_Repeatability)
            # print("varComp_reproducibility: ", varComp_reproducibility)
            # print("varComp_part_to_part: ", varComp_part_to_part)
            # print("varComp_total_RageRR: ", varComp_total_RageRR)
            # print("varComp_total_variation: ", varComp_total_variation)
            # print("Grr: ", total_RageRR * 6)
            # print("grr_tolerance: ", grr_tolerance)

        except Exception as e:
            # raise print(" -------------- Gage Variance -------------- \r\n" + str(e.args))
            print(" -------------- Gage Variance -------------- \r\n" + str(e.args))
            return np.nan
        return np.nan if math.isinf(grr_tolerance) else grr_tolerance

    @staticmethod
    def cooking_mean(arr_3d: np.array, grr_shape0, grr_shape1, grr_shape2):
        try:
            # has_nan = np.isnan(arr_3d).any()
            overall_average = np.mean(arr_3d)  # if not has_nan else None
            op_mean_lst = [np.mean(arr_3d[x]) for x in range(grr_shape2)]  # shape >>> (3, 10, 3)
            dut_op_mean_lst = [np.mean(arr_3d[i], axis=1) for i in range(grr_shape0)]
            dut_mean_lst = [np.mean([arr_3d[0][i], arr_3d[1][i], arr_3d[2][i]]) for i in range(grr_shape1)]  # Average of DUT_A, Average of DUT_B, Average of DUT_C
            # print("OP-mean", op_mean_lst)  # Average of DUT_A, Average of DUT_B, Average of DUT_C
            # print("Average of DUT:", overall_average)
            # print("dut_op_mean_lst:", dut_op_mean_lst)
            # print("dut_mean_lst:", dut_mean_lst)
        except Exception as ex:
            print(" cooking_mean NG >>> " + str(ex.args))
            return np.nan
            # raise ex.args
        return overall_average, op_mean_lst, dut_op_mean_lst, dut_mean_lst

    def cooking_grr(self):
        RR_A = []
        RR_B = []
        RR_C = []
        try:
            if self.range_spec == 0:
                raise Exception("spec_range_is_0")
            arr_3d = np.array(self.data)
            grr_shape0 = arr_3d.shape[0]
            grr_shape1 = arr_3d.shape[1]
            grr_shape2 = arr_3d.shape[2]
            # Initialize an empty array to store the converted values
            float_arr = np.empty_like(arr_3d, dtype=float)

            # Iterate through the array and convert elements to float
            for i in range(arr_3d.shape[0]):
                for j in range(arr_3d.shape[1]):
                    for k in range(arr_3d.shape[2]):
                        float_arr[i, j, k] = float(arr_3d[i, j, k])

            overall_average, op_mean_lst, dut_op_mean_lst, dut_mean_lst = Gage.cooking_mean(float_arr, grr_shape0, grr_shape1, grr_shape2)
            overall_trans = [(i - overall_average) ** 2 for i in float_arr]  # total transform
            # print("RR_trans:", overall_trans)
            for j in range(grr_shape1):
                for i in range(grr_shape2):
                    squared_diff_A = (float_arr[0][j][i] - float(dut_op_mean_lst[0][j])) ** 2
                    # print(f"squared_diff_A: ({float_arr[0][j][i]} - {dut_op_mean_lst[0][j]} )**2 ")
                    squared_diff_B = (float_arr[1][j][i] - float(dut_op_mean_lst[1][j])) ** 2
                    # print(f"squared_diff_B: ({float_arr[1][j][i]} - {dut_op_mean_lst[1][j]} )**2 ")
                    squared_diff_C = (float_arr[2][j][i] - float(dut_op_mean_lst[2][j])) ** 2
                    # print(f"squared_diff_C: ({float_arr[2][j][i]} - {dut_op_mean_lst[2][j]} )**2 ")
                    # print('-----------------------------------------')
                    RR_A.append(squared_diff_A)
                    RR_B.append(squared_diff_B)
                    RR_C.append(squared_diff_C)
            # Calculate sums of squared differences
            RR_A_sum = np.sum(RR_A)
            RR_B_sum = np.sum(RR_B)
            RR_C_sum = np.sum(RR_C)
            # print("RR_A:", RR_A_sum)
            # print("RR_B:", RR_B_sum)
            # print("RR_C:", RR_C_sum)
            # --------------------- Sum of square -----------------------------
            # number of test time of dut
            dut_test_times = int(len(float_arr[0][0])) + int(len(float_arr[1][0])) + int(len(float_arr[2][0]))
            SS_DUT = [(dut_mean_lst[i] - np.mean(dut_mean_lst)) ** 2 * dut_test_times for i in range(grr_shape1)]

            SS_OP_A = grr_shape1 * grr_shape2 * (op_mean_lst[0] - overall_average) ** 2
            SS_OP_B = grr_shape1 * grr_shape2 * (op_mean_lst[1] - overall_average) ** 2
            SS_OP_C = grr_shape1 * grr_shape2 * (op_mean_lst[2] - overall_average) ** 2
            SS_OP = np.sum([SS_OP_A, SS_OP_B, SS_OP_C])
            SS_total = np.sum(overall_trans)
            SS_Repeatability = np.sum([RR_A_sum, RR_B_sum, RR_C_sum])
            SS_DUT_op = SS_total - SS_Repeatability - SS_OP - np.sum(SS_DUT)
            # print("dut_test_times", dut_test_times)
            # print("SS_DUT: ", np.sum(SS_DUT))
            # print("SS_total: ", SS_total)
            # print("SS_OP: ", SS_OP)
            # print("SS_Repeatability: ", SS_Repeatability)
            # print("SS_DUT_op: ", SS_DUT_op)
            # --------------------- twoWay anova -----------------------------
            # Table 1 with interaction
            df_dut = grr_shape1 - 1
            df_op = grr_shape2 - 1
            df_dut_op = df_dut * df_op
            df_repeat = grr_shape0 * grr_shape1 * grr_shape2 - grr_shape0 * grr_shape1
            MS_0 = np.sum(SS_DUT) / df_dut
            MS_1 = SS_OP / df_op
            MS_2 = SS_DUT_op / df_dut_op
            MS_3 = SS_Repeatability / df_repeat
            F1 = np.nan if np.isnan(MS_0 / MS_2) else MS_0 / MS_2
            F2 = np.nan if np.isnan(MS_1 / MS_2) else MS_1 / MS_2
            F3 = np.nan if np.isnan(MS_2 / MS_3) else MS_2 / MS_3
            if np.isnan([F1, F2, F3]).any():
                return np.nan
            p_value1 = 1 - f.cdf(F1, df_dut, df_repeat)
            p_value2 = 1 - f.cdf(F2, df_op, df_repeat)
            # p_value3 = 1 - f.cdf(F3, df_dut_op, df_repeat)
            ## https: // www.geeksforgeeks.org / how - to - perform - an - f - test - in -python /
            ## Table 2 without interaction as if p_value3 >= 0.05
            if (p_value3 := 1 - f.cdf(F3, df_dut_op, df_repeat)) > 0.05:
                MS_0_t2 = np.sum(SS_DUT) / df_dut
                MS_1_t2 = SS_OP / df_op
                MS_2_t2 = (SS_DUT_op + SS_Repeatability) / (df_repeat + df_dut_op)
                F1_t2 = np.nan if np.isnan(MS_0_t2 / MS_2_t2) else MS_0_t2 / MS_2_t2
                F2_t2 = np.nan if np.isnan(MS_1_t2 / MS_2_t2) else MS_1_t2 / MS_2_t2
                p_value1_t2 = 1 - f.cdf(F1_t2, df_dut, (df_repeat + df_dut_op))
                p_value2_t2 = 1 - f.cdf(F2_t2, df_op, (df_repeat + df_dut_op))
            else:
                MS_0_t2 = np.nan
                MS_1_t2 = np.nan
                MS_2_t2 = np.nan
            # print("F1: ", F1)
            # print("F2: ", F2)
            # print("F3: ", F3)
            # print("p_value1: ", p_value1)
            # print("p_value2: ", p_value2)
            # print("p_value3: ", p_value3)
            # print("F1_t2: ", F1_t2)
            # print("F2_t2: ", F2_t2)
            # print("p_value1_t2: ", p_value1_t2)
            # print("p_value2_t2: ", p_value2_t2)
            # -------------- GRR_Variance --------------
            grr_tolerance = self.grr_variance(self.range_spec, grr_shape1, grr_shape2, MS_0, MS_1, MS_2, MS_3, MS_0_t2, MS_1_t2, MS_2_t2, p_value1, p_value3, F3)

        except RuntimeWarning as ex:
            print(f"RuntimeWarning$NG >>> " + str(ex.args))
            return np.nan
        except Exception as ex:
            print(f"cooking_grr$exception >>> " + str(ex.args))
            return np.nan
            # raise "calc failure => " + str(ex.args)
        return np.nan if np.isnan(F1) else grr_tolerance

# if __name__ == '__main__':
#     # A_op = [[1, 2, 3] for _ in range(10)] B_op = [[4, 5, 6] for _ in range(10)] C_op = [[7, 8, 9] for _ in range(
#     # 10)] A_op = [[42,42,42],[41,42,44],[44,44,44],[40,41,42],[42,41,43],[42,42,42],[40,40,39],[39,40,41],[41,41,
#     # 41],[40,40,41]] B_op = [[40,39,41],[41,41,41],[41,41,41],[41,41,42],[43,42,42],[42,42,42],[41,42,42],[43,43,
#     # 44],[40,40,42],[39,40,42]] C_op = [[41,42,42],[41,39,41],[40,42,43],[43,42,40],[39,38,38],[38,39,40],[41,40,
#     # 39],[44,43,39],[39,39,40],[40,41,40]]
#
#     A_op = [[42, 42, 42], [40, 41, 42], [40, 40, 39], [40, 40, 41], [41, 41, 41], [42, 42, 42], [40, 40, 42],
#             [41, 39, 41], [39, 38, 38], [44, 43, 39]]
#     B_op = [[41, 42, 44], [42, 41, 43], [39, 40, 41], [40, 39, 41], [41, 41, 42], [41, 42, 42], [39, 40, 42],
#             [40, 42, 43], [38, 39, 40], [39, 39, 40]]
#     C_op = [[44, 44, 44], [42, 42, 42], [41, 41, 41], [41, 41, 41], [43, 42, 42], [43, 43, 44], [41, 42, 42],
#             [43, 42, 40], [41, 40, 39], [40, 41, 40]]
#
#     DUT_1 = [A_op, B_op, C_op]
#     # print(DUT_1)
#     grr_instance = Gage(DUT_1, -5, 5)
#     grr_instance.rawData_handling(DUT_1)
