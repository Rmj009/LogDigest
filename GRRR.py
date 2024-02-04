import numpy as np
from scipy.stats import f

def calc_grr(*args):
    # A_op = np.array(self.data)
    # B_op = np.array(self.data)
    # C_op = np.array(self.data)
    try:
        arr_2d = np.array(args)
        overall_average = np.mean(arr_2d)

        # Calculate the average along axis 0 (column-wise)
        average_axis_0 = np.mean(arr_2d, axis=0)

        print("Average along axis 0:", average_axis_0)

        # Calculate the average along axis 1 (row-wise)
        average_axis_1 = np.mean(arr_2d, axis=1)

        print("Average along axis 1:", average_axis_1)

        print("Average of DUT:", overall_average)

        # Initialize arrays to store squared differences
        RR_A = []
        RR_B = []
        RR_C = []
        RR_mean = [np.mean(i, 1) for i in arr_2d]
        RR_trans = [(i - overall_average) ** 2 for i in arr_2d]
        print("RR_mean:", RR_mean)
        print("RR_trans:", RR_trans)

        # Calculate squared differences for each element in the first row
        for i in range(arr_2d.shape[1]):
            squared_diff_A = (arr_2d[0][0][i] - int(RR_mean[0][0])) ** 2
            squared_diff_B = (arr_2d[0][1][i] - int(RR_mean[0][1])) ** 2
            squared_diff_C = (arr_2d[0][2][i] - int(RR_mean[0][2])) ** 2
            RR_A.append(squared_diff_A)
            RR_B.append(squared_diff_B)
            RR_C.append(squared_diff_C)

        # Calculate sums of squared differences
        RR_A_sum = np.sum(RR_A)
        RR_B_sum = np.sum(RR_B)
        RR_C_sum = np.sum(RR_C)

        print("RR_A:", RR_A_sum)
        print("RR_B:", RR_B_sum)
        print("RR_C:", RR_C_sum)
        # --------------------- Sum of square -----------------------------
        # RR_1 = []
        # RR_1.append(RR_A_sum)
        # B2 = np.mean([DUT_1_array])  # B2
        # print("____", B2)

    except Exception as ex:
        print(f"calc" + str(ex.args))
        raise "calc failure => " + str(ex.args)


def rawData_handling(*args):
    # A_op = np.array(self.data)
    # B_op = np.array(self.data)
    # C_op = np.array(self.data)
    try:
        arr_3d = np.array(args)
        # print(arr_3d.shape)
        overall_average = np.mean(arr_3d)
        print("Average of DUT:", overall_average)
        op_mean_lst = [np.mean(arr_3d[0][x]) for x in range(arr_3d.shape[1])]  # shape >>> (1, 3, 10, 3)

        print("OP-mean", op_mean_lst)

        # Initialize arrays to store squared differences
        RR_A = []
        RR_B = []
        RR_C = []
        dut_op_mean_lst = [np.mean(arr_3d[0][i], axis=1) for i in range(arr_3d.shape[1])]
        # [np.mean(arr_3d[0][i][j], 0) for j in range(arr_3d.shape[2]) for i in range(arr_3d.shape[3])]
        # Average of DUT_A, Average of DUT_B, Average of DUT_C
        print("dut_op_mean_lst:", dut_op_mean_lst)
        overall_trans = [(i - overall_average) ** 2 for i in arr_3d]  # total transform
        # print("RR_trans:", overall_trans)

        # Calculate squared differences for each element in the first row
        for i in range(arr_3d.shape[2]):
            for j in range(arr_3d.shape[3]):
                squared_diff_A = (arr_3d[0][0][i][j] - int(dut_op_mean_lst[0][j])) ** 2
                squared_diff_B = (arr_3d[0][1][i][j] - int(dut_op_mean_lst[1][j])) ** 2
                squared_diff_C = (arr_3d[0][2][i][j] - int(dut_op_mean_lst[2][j])) ** 2
                RR_A.append(squared_diff_A)
                RR_B.append(squared_diff_B)
                RR_C.append(squared_diff_C)

        # Calculate sums of squared differences
        RR_A_sum = np.sum(RR_A)
        RR_B_sum = np.sum(RR_B)
        RR_C_sum = np.sum(RR_C)

        print("RR_A:", RR_A_sum)
        print("RR_B:", RR_B_sum)
        print("RR_C:", RR_C_sum)
        # --------------------- Sum of square -----------------------------
        dut_mean_lst = [np.mean([arr_3d[0][0][i], arr_3d[0][1][i], arr_3d[0][2][i]]) for i in range(arr_3d.shape[2])]
        # Average of DUT_A, Average of DUT_B, Average of DUT_C
        print("dut_mean_lst:", dut_mean_lst)
        SS_DUT = [(dut_mean_lst[i] - np.average(dut_mean_lst)) ** 2 * arr_3d.shape[2] for i in range(arr_3d.shape[2])]
        print("SS_DUT: ", np.mean(SS_DUT))

        SS_OP_A = arr_3d.shape[2] * arr_3d.shape[3] * (op_mean_lst[0] - overall_average) ** 2
        SS_OP_B = arr_3d.shape[2] * arr_3d.shape[3] * (op_mean_lst[1] - overall_average) ** 2
        SS_OP_C = arr_3d.shape[2] * arr_3d.shape[3] * (op_mean_lst[2] - overall_average) ** 2
        SS_OP = np.sum([SS_OP_A, SS_OP_B, SS_OP_C])
        print("SS_DUT: ", SS_OP)

        SS_total = np.sum(overall_trans)
        print("SS_total: ", SS_total)

        SS_Repeatability = np.sum([RR_A_sum, RR_B_sum, RR_C_sum])
        print("SS_total: ", SS_Repeatability)

        SS_DUT_op = SS_total - SS_Repeatability - SS_OP - np.mean(SS_DUT)
        print("SS_DUT_op: ", SS_DUT_op)

        # --------------------- twoWay anova -----------------------------
        # Table 1 with interaction
        df_dut = arr_3d.shape[2] - 1
        df_op = arr_3d.shape[3] - 1
        df_dut_op = df_dut * df_op
        df_repeat = arr_3d.shape[1] * arr_3d.shape[2] * arr_3d.shape[3] - arr_3d.shape[1] * arr_3d.shape[2]
        MS_0 = np.mean(SS_DUT) / df_dut
        print("MS_0: ", MS_0)
        MS_1 = SS_OP / df_op
        print("MS_1: ", MS_1)
        MS_2 = SS_DUT_op / df_dut_op
        print("MS_2: ", MS_2)
        MS_3 = SS_Repeatability / df_repeat
        print("MS_3: ", MS_3)
        F1 = np.nan if np.isnan(MS_0 / MS_2) else MS_0 / MS_2
        # print("F1: ", F1)
        F2 = np.nan if np.isnan(MS_1 / MS_2) else MS_1 / MS_2
        print("F2: ", F2)
        F3 = np.nan if np.isnan(MS_2 / MS_3) else MS_2 / MS_3
        print("F3: ", F3)
        # p_value1 = f.pdf(F1, df_dut, df_repeat)
        # p_value2 = f.pdf(F2, df_op, df_repeat)
        p_value3 = f.pdf(F3, df_dut_op, df_repeat)
        print("p_value3: ", p_value3)

        # Table 2 without interaction as if p_value3 >= 0.05
        MS_0_t2 = np.mean(SS_DUT) / df_dut
        print("MS_0_t2: ", MS_0_t2)
        MS_1_t2 = SS_OP / df_op
        print("MS_1_t2: ", MS_1_t2)
        MS_2_t2 = (SS_DUT_op + SS_Repeatability) / (df_repeat + df_dut_op)
        print("MS_2_t2: ", MS_2_t2)
        F1_t2 = np.nan if np.isnan(MS_0_t2 / MS_2_t2) else MS_0_t2 / MS_2_t2
        print("F1_t2: ", F1_t2)
        F2_t2 = np.nan if np.isnan(MS_1_t2 / MS_2_t2) else MS_1_t2 / MS_2_t2
        print("F2_t2: ", F2_t2)
        p_value1_t2 = f.pdf(F1_t2, df_dut, (df_repeat + df_dut_op))
        print("p_value1_t2: ", p_value1_t2)
        p_value2_t2 = f.pdf(F2_t2, df_op, (df_repeat + df_dut_op))
        print("p_value2_t2: ", p_value2_t2)

        # -------------- GRR_Variance --------------
        Repeatability = 0 if F3 > 0.05 else MS_3
        print("Repeatability: ", Repeatability)
        isGreater = MS_2 - MS_3 > 0
        print("isGreater: ", isGreater)

        # Reproduability = 0 if F3 > 0.05 else MS_3
        # varComp_op =
        # varComp_op_dut = 0 if F3 > 0.05 else MS_3
        # varComp_part_to_part =
        # varComp_total_varation =





    except RuntimeWarning as runex:
        raise "divide failure => " + str(runex.args)
    except Exception as ex:
        print(f"calc" + str(ex.args))
        raise "calc failure => " + str(ex.args)


class GRR:
    def __init__(self, data):  # semaphore
        self.data = data
        # self.semaphore = semaphore


if __name__ == '__main__':
    A_op = [[1, 2, 3] for _ in range(10)]
    B_op = [[4, 5, 6] for _ in range(10)]
    C_op = [[7, 8, 9] for _ in range(10)]
    DUT_1 = [A_op, B_op, C_op]
    # print(DUT_1)
    grr_instance = GRR(DUT_1)
    rawData_handling(DUT_1)
