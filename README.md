#backup parser log script
;--------------------------------------
import os
import csv


def gather_lines_containing_string(directory_path, string_to_find, output_csv_path):
    # Open CSV file for writing
    with open(output_csv_path, 'w', newline='', encoding='utf-16') as csvfile:
        csv_writer = csv.writer(csvfile)

        # Write header to CSV file
        csv_writer.writerow(['File', 'Line'])

        # Iterate through files in the specified directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Check if the path is a file
            if os.path.isfile(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-16') as file:
                        # Iterate through lines in the file
                        for line_number, line in enumerate(file, start=1):
                            # Check if the line contains the specified string
                            if string_to_find in line:
                                # Write the file name and line to the CSV file
                                csv_writer.writerow([filename, f'Line {line_number}: {line.strip()}'])
                except UnicodeDecodeError:
                    print(f"Error decoding file {filename}. Skipping...")


def fetch_concentrate():
    print("fetch all directory log keyword and log timeStamp")

    print("merge all into one csv")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    directory_path = "D:\DataSystem_NPI_v2.0.4_20230421\ATS_Log\ove700"
    string_to_find = "FactoryReset SPEC:0~0 Value:0"
    output_csv_path = "FactoryReset700.csv"

    gather_lines_containing_string(directory_path, string_to_find, output_csv_path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
