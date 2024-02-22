import datetime as dt
import numpy as np
from scipy.stats import f


class Gage:
    def __init__(self, data, LSL, USL):
        self.data = data
        self.USL = USL
        self.LSL = LSL
        self.range_spec = self.USL - self.LSL

    def fmt_println(self):
        print(self.USL, self.LSL, self.range_spec)

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

    def rawData_handling(self, *args):
        # A_op = np.array(self.data)
        # B_op = np.array(self.data)
        # C_op = np.array(self.data)
        try:
            arr_3d = np.array(self.data)
            # print(arr_3d.shape)
            overall_average = np.mean(arr_3d)
            print("Average of DUT:", overall_average)
            op_mean_lst = [np.mean(arr_3d[x]) for x in range(arr_3d.shape[2])]  # shape >>> (3, 10, 3)

            print("OP-mean", op_mean_lst)

            # Initialize arrays to store squared differences
            RR_A = []
            RR_B = []
            RR_C = []
            dut_op_mean_lst = [np.mean(arr_3d[i], axis=1) for i in range(arr_3d.shape[0])]
            # [np.mean(arr_3d[0][i][j], 0) for j in range(arr_3d.shape[2]) for i in range(arr_3d.shape[3])]
            # Average of DUT_A, Average of DUT_B, Average of DUT_C
            print("dut_op_mean_lst:", dut_op_mean_lst)
            overall_trans = [(i - overall_average) ** 2 for i in arr_3d]  # total transform
            # print("RR_trans:", overall_trans)

            # Calculate squared differences for each element in the first row
            for j in range(arr_3d.shape[1]):
                for i in range(arr_3d.shape[2]):
                    squared_diff_A = (arr_3d[0][j][i] - float(dut_op_mean_lst[0][j])) ** 2
                    print(f"squared_diff_A: ({arr_3d[0][j][i]} - {dut_op_mean_lst[0][j]} )**2 ")
                    squared_diff_B = (arr_3d[1][j][i] - float(dut_op_mean_lst[1][j])) ** 2
                    print(f"squared_diff_B: ({arr_3d[1][j][i]} - {dut_op_mean_lst[1][j]} )**2 ")
                    squared_diff_C = (arr_3d[2][j][i] - float(dut_op_mean_lst[2][j])) ** 2
                    print(f"squared_diff_C: ({arr_3d[2][j][i]} - {dut_op_mean_lst[2][j]} )**2 ")
                    print('-----------------------------------------')
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
            dut_mean_lst = [np.mean([arr_3d[0][i], arr_3d[1][i], arr_3d[2][i]]) for i in
                            range(arr_3d.shape[1])]
            # Average of DUT_A, Average of DUT_B, Average of DUT_C
            print("dut_mean_lst:", dut_mean_lst)
            # number of test time of dut
            dut_test_times = int(len(arr_3d[0][0])) + int(len(arr_3d[1][0])) + int(len(arr_3d[2][0]))
            print("dut_test_times", dut_test_times)
            SS_DUT = [(dut_mean_lst[i] - np.mean(dut_mean_lst)) ** 2 * dut_test_times for i in
                      range(arr_3d.shape[1])]
            print("SS_DUT: ", np.sum(SS_DUT))

            SS_OP_A = arr_3d.shape[1] * arr_3d.shape[2] * (op_mean_lst[0] - overall_average) ** 2
            SS_OP_B = arr_3d.shape[1] * arr_3d.shape[2] * (op_mean_lst[1] - overall_average) ** 2
            SS_OP_C = arr_3d.shape[1] * arr_3d.shape[2] * (op_mean_lst[2] - overall_average) ** 2
            SS_OP = np.sum([SS_OP_A, SS_OP_B, SS_OP_C])
            SS_total = np.sum(overall_trans)
            SS_Repeatability = np.sum([RR_A_sum, RR_B_sum, RR_C_sum])
            SS_DUT_op = SS_total - SS_Repeatability - SS_OP - np.sum(SS_DUT)

            print("SS_OP: ", SS_OP)
            # print("SS_total: ", SS_total)
            print("SS_Repeatability: ", SS_Repeatability)
            print("SS_DUT_op: ", SS_DUT_op)

            # --------------------- twoWay anova -----------------------------
            # Table 1 with interaction
            df_dut = arr_3d.shape[1] - 1
            df_op = arr_3d.shape[2] - 1
            df_dut_op = df_dut * df_op
            df_repeat = arr_3d.shape[0] * arr_3d.shape[1] * arr_3d.shape[2] - arr_3d.shape[0] * arr_3d.shape[1]
            MS_0 = np.sum(SS_DUT) / df_dut
            MS_1 = SS_OP / df_op
            MS_2 = SS_DUT_op / df_dut_op
            MS_3 = SS_Repeatability / df_repeat
            F1 = np.nan if np.isnan(MS_0 / MS_2) else MS_0 / MS_2
            F2 = np.nan if np.isnan(MS_1 / MS_2) else MS_1 / MS_2
            F3 = np.nan if np.isnan(MS_2 / MS_3) else MS_2 / MS_3
            p_value1 = 1 - f.cdf(F1, df_dut, df_repeat)  # 0.6524410065803709
            p_value2 = 1 - f.cdf(F2, df_op, df_repeat)
            p_value3 = 1 - f.cdf(F3, df_dut_op, df_repeat)
            ## https: // www.geeksforgeeks.org / how - to - perform - an - f - test - in -python /
            ## Table 2 without interaction as if p_value3 >= 0.05
            MS_0_t2 = np.sum(SS_DUT) / df_dut
            MS_1_t2 = SS_OP / df_op
            MS_2_t2 = (SS_DUT_op + SS_Repeatability) / (df_repeat + df_dut_op)
            F1_t2 = np.nan if np.isnan(MS_0_t2 / MS_2_t2) else MS_0_t2 / MS_2_t2
            F2_t2 = np.nan if np.isnan(MS_1_t2 / MS_2_t2) else MS_1_t2 / MS_2_t2
            p_value1_t2 = 1 - f.cdf(F1_t2, df_dut, (df_repeat + df_dut_op))
            p_value2_t2 = 1 - f.cdf(F2_t2, df_op, (df_repeat + df_dut_op))
            # print("MS_0: ", MS_0)
            # print("MS_1: ", MS_1)
            # print("MS_2: ", MS_2)
            # print("MS_3: ", MS_3)
            print("F1: ", F1)
            print("F2: ", F2)
            print("F3: ", F3)
            print("p_value1: ", p_value1)
            print("p_value2: ", p_value2)
            print("p_value3: ", p_value3)

            # print("MS_0_t2: ", MS_0_t2)
            # print("MS_1_t2: ", MS_1_t2)
            # print("MS_2_t2: ", MS_2_t2)
            print("F1_t2: ", F1_t2)
            print("F2_t2: ", F2_t2)
            print("p_value1_t2: ", p_value1_t2)
            print("p_value2_t2: ", p_value2_t2)
            print('-----------------------------------------')
            # -------------- GRR_Variance --------------
            varComp_Repeatability = 0 if F3 > 0.05 else MS_3

            isGreater = MS_2 - MS_3 > 0
            # print("isGreater: ", isGreater)

            if MS_1_t2 > MS_2_t2:
                ans1 = (MS_1_t2 - MS_2_t2) / (arr_3d.shape[1] * arr_3d.shape[2])
            else:
                ans1 = 0
            if MS_1 > MS_2:
                ans2 = (MS_1 - MS_2) / (arr_3d.shape[1] * arr_3d.shape[2])
            else:
                ans2 = 0

            if p_value3 > 0.05:
                print("p_value greater than alpha 0.05")
                varComp_op = ans1
                print("varComp_op: ", varComp_op)
                # ------------
                varComp_op_dut = 0
                print("varComp_op_dut: ", varComp_op_dut)
                # ------------
                if MS_0_t2 > MS_1_t2:
                    varComp_part_to_part = (MS_0_t2 - MS_2_t2) / (3 * 3)  # ???????
                else:
                    varComp_part_to_part = 0
                    print("varComp_part_to_part: ", varComp_part_to_part)

            else:
                varComp_op = ans2
                print("varComp_op: ", varComp_op)
                # -----------
                varComp_op_dut = (MS_3 - MS_2) / arr_3d.shape[2]
                print("varComp_op_dut: ", varComp_op_dut)
                # -----------
                if MS_0 > MS_3:
                    varComp_part_to_part = (MS_0 - MS_2) / (3 * 3)  # ???????
                else:
                    varComp_part_to_part = 0

            varComp_reproducibility = varComp_op if F3 > 0.05 else (varComp_op + varComp_op_dut)
            varComp_total_RageRR = varComp_reproducibility + varComp_Repeatability
            varComp_total_variation = varComp_total_RageRR + varComp_part_to_part
            # total_GageRR = (varComp_reproducibility ** 2 + varComp_Repeatability ** 2) ** (1 / 2)
            print("varComp_Repeatability: ", varComp_Repeatability)
            print("varComp_reproducibility: ", varComp_reproducibility)
            print("varComp_part_to_part: ", varComp_part_to_part)
            print("varComp_total_RageRR: ", varComp_total_RageRR)
            print("varComp_total_variation: ", varComp_total_variation)
            # print("total_GageRR: ", total_GageRR)
            result = (varComp_Repeatability, varComp_reproducibility, varComp_op, varComp_op_dut, varComp_part_to_part,
                      varComp_total_RageRR)
            # Gage.grr_contribution(self, result)
            reproducibility = varComp_op if p_value1 > 0.05 else (varComp_op + varComp_op_dut)
            repeatability = varComp_Repeatability ** (1 / 2)
            total_RageRR = (reproducibility ** 2 + repeatability ** 2) ** (1 / 2)
            print("Grr: ", total_RageRR * 6)
            grr_tolerance = total_RageRR * 6 / self.range_spec * 100
            print("grr_tolerance: ", grr_tolerance)

        except RuntimeWarning as ex:
            raise "divide failure => " + str(ex.args)
        except Exception as ex:
            print(f"calc" + str(ex.args))
            raise "calc failure => " + str(ex.args)
        return grr_tolerance


if __name__ == '__main__':
    # A_op = [[1, 2, 3] for _ in range(10)] B_op = [[4, 5, 6] for _ in range(10)] C_op = [[7, 8, 9] for _ in range(
    # 10)] A_op = [[42,42,42],[41,42,44],[44,44,44],[40,41,42],[42,41,43],[42,42,42],[40,40,39],[39,40,41],[41,41,
    # 41],[40,40,41]] B_op = [[40,39,41],[41,41,41],[41,41,41],[41,41,42],[43,42,42],[42,42,42],[41,42,42],[43,43,
    # 44],[40,40,42],[39,40,42]] C_op = [[41,42,42],[41,39,41],[40,42,43],[43,42,40],[39,38,38],[38,39,40],[41,40,
    # 39],[44,43,39],[39,39,40],[40,41,40]]

    A_op = [[42, 42, 42], [40, 41, 42], [40, 40, 39], [40, 40, 41], [41, 41, 41], [42, 42, 42], [40, 40, 42],
            [41, 39, 41], [39, 38, 38], [44, 43, 39]]
    B_op = [[41, 42, 44], [42, 41, 43], [39, 40, 41], [40, 39, 41], [41, 41, 42], [41, 42, 42], [39, 40, 42],
            [40, 42, 43], [38, 39, 40], [39, 39, 40]]
    C_op = [[44, 44, 44], [42, 42, 42], [41, 41, 41], [41, 41, 41], [43, 42, 42], [43, 43, 44], [41, 42, 42],
            [43, 42, 40], [41, 40, 39], [40, 41, 40]]

    DUT_1 = [A_op, B_op, C_op]
    # print(DUT_1)
    grr_instance = Gage(DUT_1, -5, 5)
    grr_instance.rawData_handling(DUT_1)
