import pandas as pd


class CleanUp(object):
    global spec_range

    def __init__(self, file_path):
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

    def washing(self):
        # d_path = "C:\Users\23002496\PycharmProjects\DigestATSuite\IMQX.csv"
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        spec_lst = []
        spec_lst2 = []
        values_lst = []
        values_lst2 = []
        try:
            with open(self.file_path, mode='r', encoding='utf-16', errors='ignore') as file:
                # Create a CSV reader object
                lines = file.readlines()
                for line in lines:
                    # Find the indices of the keywords in the line
                    index1 = line.find(keyword1)
                    index2 = line.find(keyword2)
                    index3 = line.find(keyword2, index1 + len(keyword1))

                    # Extract the substring between the keywords if both keywords are found
                    if index1 != -1 and index2 != -1:
                        spec_range = line[index1 + len(keyword1):index2].strip()
                        spec_values = line[index2 + len(keyword2):].strip()
                        if len(spec_lst) > 10000:
                            spec_lst2.append(spec_range)
                            values_lst2.append(spec_values)
                        spec_lst.append(spec_range)
                        values_lst.append(spec_values)
                s = pd.Series(spec_lst)
                v = pd.Series(values_lst)
                s2 = pd.Series(spec_lst2)
                v2 = pd.Series(values_lst2)
                df = pd.DataFrame([s, s2, v, v2])
                df = df.T
                df.to_csv("iiii.csv", sep=',')
            file.close()

        except Exception as e:
            raise "NG" + str(e.args)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # filename = input("csv name")
    filename = 'C:\\Users\\23002496\\PycharmProjects\\DigestATSuite\\IMQX.txt'
    ats_instance = CleanUp(filename)
    ats_instance.washing()
    # directory_path = "D:\DataSystem_NPI_v2.0.4_20230421\ATS_Log\Breakdown"
    # directory_path = "D:\Analysis tool 20230321\ParseLog\IMQX"
    # string_to_find = "SPEC:"
    # string_to_find2 = "Value:"
    # output_csv_path = "IMQX.csv"

    # gather_lines_containing_string(directory_path, string_to_find, string_to_find2, output_csv_path)

    # ----------------------------------------------------------

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
