import numpy as np
import pandas as pd


class CleanUp(object):

    def __init__(self, file_path, spec_range):
        self.spec_range = spec_range
        self.file_path = file_path

    # def gather_lines_containing_string(directory_path, string_to_find, string_to_find2, output_csv_path):
    #     # Open CSV file for writing
    #     with open(output_csv_path, 'w', newline='', encoding='utf-16') as csvfile:
    #         csv_writer = csv.writer(csvfile)
    #         # # Write header to CSV file
    #         # csv_writer.writerow(['File', 'Line'])
    #         # Iterate through files in the specified directory
    #         for filename in os.listdir(directory_path):
    #             file_path = os.path.join(directory_path, filename)
    #
    #             # Check if the path is a file
    #             if os.path.isfile(file_path):
    #                 digestFiles(file_path, csv_writer, filename)

    # def digestFiles(file_path, csv_writer, filename):
    #     try:
    #         with open(file_path, 'r', encoding='utf-16') as file:
    #             # Iterate through lines in the file
    #             for line_number, line in enumerate(file, start=1):
    #                 # Check if the line contains the specified string
    #                 if string_to_find in line and string_to_find2 in line:
    #                     # Write the file name and line to the CSV file
    #                     csv_writer.writerow([filename, f'{line.strip()}'])
    #     except UnicodeDecodeError:
    #                     print(f"Error decoding file {filename}. Skipping...")

    @staticmethod
    def washing_spec(self, *args):
        spec_lst = args
        try:
            self.spec_range = spec_lst if self.spec_range is None else None

        except Exception as e:
            raise "washing_spec$NG >>> " + str(e.args)

    def washing(self):
        """
        Diagnosis >>> count test items
        :return:
        """
        # d_path = "C:\Users\23002496\PycharmProjects\DigestATSuite\IMQX.csv"
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        specRange = ""
        testItem_values = ""
        all_lst = []
        spec_lst = []
        data_lst = []
        values_lst = []
        countTestItems = 5810
        IsSpecRange_ready = False
        # countStressTimes = 10  # num_lst = 0
        try:
            with open(self.file_path, mode='r', encoding='utf-16', errors='ignore') as file:
                # Create a CSV reader object
                lines = file.readlines()
                for line in lines:
                    if len(data_lst) < countTestItems:
                        # Find the indices of the keywords in the line
                        index1 = line.find(keyword1)
                        index2 = line.find(keyword2)
                        # index3 = line.find(keyword2, index1 + len(keyword1))
                        if index1 != -1 and index2 != -1:
                            specRange = line[index1 + len(keyword1):index2].strip()
                            testItem_values = line[index2 + len(keyword2):].strip()
                            data_lst.append(testItem_values)
                            if not IsSpecRange_ready:
                                spec_lst.append(specRange)
                    else:
                        # acquire spec_lst once
                        IsSpecRange_ready = True
                        all_lst.append(data_lst)
                        data_lst = []
                df = pd.DataFrame(np.array(all_lst))
                df = df.T
                df['spec'] = pd.Series(spec_lst)
                df.to_csv("IMQX_sample.csv", sep=',')
            file.close()

        except Exception as e:
            raise "NG" + str(e.args)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # filename = input("csv name: \r\n")
    filename = 'C:\\Users\\23002496\\PycharmProjects\\DigestATSuite\\IMQX.txt'
    ats_instance = CleanUp(filename, None)
    ats_instance.washing()
    # directory_path = "D:\DataSystem_NPI_v2.0.4_20230421\ATS_Log\Breakdown"
    # directory_path = "D:\Analysis tool 20230321\ParseLog\IMQX"
    # string_to_find = "SPEC:"
    # string_to_find2 = "Value:"
    # output_csv_path = "IMQX.csv"

    # gather_lines_containing_string(directory_path, string_to_find, string_to_find2, output_csv_path)
