import numpy as np


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


class GRR:
    def __init__(self, data):  # semaphore
        self.data = data
        # self.semaphore = semaphore


if __name__ == '__main__':
    A_op = [1, 2, 3]
    B_op = [4, 5, 6]
    C_op = [7, 8, 9]
    DUT_1 = [A_op, B_op, C_op]
    grr_instance = GRR(DUT_1)
    calc_grr(DUT_1)
