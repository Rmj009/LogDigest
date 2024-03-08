import csv
import os
import re
import numpy as np
import pandas as pd

from DelightXlsx import XlsxManager
global countTestItems


class CleanUp(object):

    def __init__(self, file_path, ending_keyword):
        self.ending_keyword = ending_keyword
        # self.spec_range = spec_range
        self.file_path = file_path
        self.countTestItems = 5810  # get num since open & parse txt

    @staticmethod
    def gather_lines_containing_string(directory_path, output_csv_path):
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        try:
            with open(output_csv_path, 'w', newline='', encoding='utf-16') as txtFile:
                # csv_writer = csv.writer(csvfile)
                # Iterate through files in the specified directory
                for filename in os.listdir(directory_path):
                    file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-16') as file:
                        for line_number, line in enumerate(file, start=1):
                            if keyword1 in line and keyword2 in line:
                                txtFile.write(f'{line.strip()}\n')
                                # Write the file name and line to the CSV file
                                # csv_writer.writerow([file_name, f'{line.strip()}'])
        except UnicodeDecodeError:
            print(f"Error decoding file {file}. Skipping...")
        except Exception as e:
            raise "digestFiles$NG >>> " + str(e.args)
        print("----------------")

    def digestFiles(self, file_path, csv_writer, file_name):
        string_to_find = "SPEC:"
        string_to_find2 = "Value:"
        try:
            with open(file_path, 'r', encoding='utf-16') as file:
                # Iterate through lines in the file
                for line_number, line in enumerate(file, start=1):
                    # Check if the line contains the specified string
                    if string_to_find in line and string_to_find2 in line:
                        # Write the file name and line to the CSV file
                        csv_writer.writerow([file_name, f'{line.strip()}'])
        except UnicodeDecodeError:
            print(f"Error decoding file {file_name}. Skipping...")
        except Exception as e:
            raise "digestFiles$NG >>> " + str(e.args)

    def txt_rush(self):
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        ending_keyword = "END MARKED"
        USL_lst = []
        LSL_lst = []
        testItem_lst = []
        try:
            with open(self.file_path, mode='r', encoding='utf-16', errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    if line.find(ending_keyword):  # stop reading til the end keyword
                        break
                    # Find the indices of the keywords in the line
                    index1 = line.find(keyword1)
                    index2 = line.find(keyword2)
                    # index3 = line.find(keyword2, index1 + len(keyword1))
                    test_item_name = line[:index1].strip(' ').split(' ')[-1]
                    testItem_lst.append(test_item_name)
                    specRange = line[index1 + len(keyword1):index2].strip()
                    # specRange = "PASS~PASS" if specRange == "PASS" else None
                    if specRange == "PASS":
                        USL_lst.append("PASS")
                        LSL_lst.append("PASS")
                    else:
                        LSL_lst.append(specRange.split('~')[0])
                        USL_lst.append(specRange.split('~')[1])
                # if index1 != -1 and index2 != -1:
                #     testItem_values = line[index2 + len(keyword2):].strip()
                #     data_lst.append(testItem_values)
        except Exception as e:
            raise "Open txt NG >>> " + str(e.args)

    def washing(self):
        """
        Diagnosis >>> count test items
        :return:
        """
        self.file_path = "C:\\Users\\23002496\\PycharmProjects\\DigestATSuite\\IMQX.csv"
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        specRange = ""
        pattern = r"~"
        testItem_values = ""
        all_lst = []
        USL_lst = []
        LSL_lst = []
        data_lst = []
        testItem_lst = []
        countTestItems = 5810
        IsSpecRange_ready = False
        # countStressTimes = 10  # num_lst = 0
        try:
            with open(self.file_path, mode='r', encoding='utf-16', errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    if len(data_lst) < countTestItems:
                        # Find the indices of the keywords in the line
                        index1 = line.find(keyword1)
                        index2 = line.find(keyword2)
                        # index3 = line.find(keyword2, index1 + len(keyword1))
                        if not IsSpecRange_ready:
                            test_item_name = line[:index1].strip(' ').split(' ')[-1]
                            testItem_lst.append(test_item_name)
                            specRange = line[index1 + len(keyword1):index2].strip()
                            if not re.search(pattern, specRange):
                                USL_lst.append("PASS")
                                LSL_lst.append("PASS")
                            else:
                                LSL_lst.append(specRange.split('~')[0])
                                USL_lst.append(specRange.split('~')[1])
                        if index1 != -1 and index2 != -1:
                            testItem_values = line[index2 + len(keyword2):].strip()
                            data_lst.append(testItem_values)
                    else:
                        IsSpecRange_ready = True
                        all_lst.append(data_lst)
                        data_lst = []
                df = pd.DataFrame(np.array(all_lst))
                df.index = (df.index[0:] + 2).tolist()
                df.loc[0] = pd.Series(LSL_lst)  # insert SPEC
                df.loc[1] = pd.Series(USL_lst)  # insert SPEC
                df = df.sort_index()
                df.columns = pd.Series(testItem_lst)  # insert test item name
                df = df.T
                # XlsxManager.cooking_CPK(None, df)
                df.to_csv("IMQX_sample.csv", sep=',')
            file.close()

        except Exception as e:
            raise "washing$NG >>> " + str(e.args)


if __name__ == '__main__':
    # filename = input("csv name: \r\n")
    # directory_path = "D:\DataSystem_NPI_v2.0.4_20230421\ATS_Log\Breakdown"
    filename = 'C:\\Users\\23002496\\PycharmProjects\\DigestATSuite\\IMQX.txt'
    directory_path = "D:\Analysis_tool_20230321\ParseLog\IMQX"
    output_csv_path = "IMQX.csv"
    """
    * 防呆(開錯檔案或ANSI CODE不相容), 分散計算
    1. open
    2. calc
    """
    ats_instance = CleanUp(filename, None)
    ats_instance.gather_lines_containing_string(directory_path, output_csv_path)
    ats_instance.washing()
