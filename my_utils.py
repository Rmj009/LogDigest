import io
import os
import re
import datetime
import numpy as np
import pandas as pd

from DelightXlsx import XlsxManager
from Gage import Gage

global countTestItems
global LSL_lst
global USL_lst
global testItem_lst


class Digest_utils(object):
    def __int__(self, filepath):
        self.filepath = filepath

    def grr_calculation(data: np.array, spec_range) -> str:
        """
        loop columns to calc
        """
        try:
            USL = float(spec_range[0])
            LSL = float(spec_range[1])
            # df_testItem = pd.DataFrame(np.array(df.iloc[:, col_nth]).reshape(10, 9))
            df_testItem = pd.DataFrame(data)
            # df_testItem = df_testItem.T
            df_testItem.columns = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
            df_testItem.index = [i for i in range(10)]
            A_op = df_testItem.iloc[:, :3].values
            B_op = df_testItem.iloc[:, 3:6].values
            C_op = df_testItem.iloc[:, 6:].values
            # a = np.all(grr_data == np.swapaxes(df_testItem.values, 1, 0))
            grr_data = [A_op, B_op, C_op]

            grr_instance = Gage(grr_data, LSL, USL)
            grr_value = grr_instance.cooking_grr(grr_data)
        except Exception as e:
            raise "grr_calculation NG >>> " + str(e.args)
        return grr_value

    def grr_cooking(self, pwd: str, csv_path, avg_weigh):
        """
        split dataframe into A,B,C blocks
        :return:
        """
        grr_lst = [f'GRR{avg_weigh}']
        avg_lst = [f'AVG{avg_weigh}']

        try:

            csv_data_path = os.path.join(pwd, "DataCSV")
            if not os.path.exists(csv_data_path):
                os.mkdir(csv_data_path)
            df = pd.read_csv(f'{csv_path}', header=0, index_col=0)
            spec_array = df.iloc[[0, 1]].values[:, 1:]
            df = df.iloc[2:, :-1]  # ignore last column
            for i in range(df.shape[1] - 1):
                select_arr_ith = np.array(df.iloc[:, i + 1]).reshape(10, 9)
                avg_lst.append(np.mean(select_arr_ith))
                grr_lst.append(Digest_utils.grr_calculation(select_arr_ith, spec_array[:, i]))
            # df_result = pd.concat([df.iloc[:3], result, df.iloc[3:]]).reset_index(drop=True)

        except Exception as e:
            raise "grr_cooking NG >>> " + str(e.args)
        return self.grr_packing(pwd, csv_path, avg_lst, grr_lst, avg_weigh)

    def grr_packing(self, *args):
        pwd, csv_path, avg_lst, grr_lst, avg_weigh = args
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(f'%H%M%S')
        try:
            summary_path = os.path.join(pwd, "Summary")
            df_pack = pd.read_csv(f'{csv_path}', header=0)
            df_pack = df_pack.iloc[:, :-1]  # remove last col fixture
            # grr_lst = [np.nan if val == 'NAN' else float(val) for val in grr_lst]
            grr_lst.insert(0, f'GRR{avg_weigh}')  # GRR as row name
            avg_lst.insert(0, f'AVG{avg_weigh}')  # AVG as row name
            #  ------------- add AVG attribute -------------
            df_pack.index = df_pack.index[:2].tolist() + (df_pack.index[2:] + 2).tolist()
            df_pack.loc[3] = np.array(avg_lst)
            df_pack.loc[2] = np.array(grr_lst)
            #  ------------- add GRR attribute -------------
            # df_pack.index = df_pack.index[:2].tolist() + (df_pack.index[2:] + 1).tolist()
            # df_pack.loc[2] = np.array(grr_lst)
            df_pack = df_pack.sort_index()
            summary_file_path = os.path.join(summary_path, f'GRR_avg{avg_weigh}_{formatted_time}.csv')
            df_pack.to_csv(summary_file_path, sep=',')
        except Exception as e:
            raise "grr_packing NG >>>" + str(e.args)

    def grr_data_digest(self, *args, **kwargs) -> np.array:
        filepath, pwd = args

        try:
            csv_data_path = os.path.join(pwd, "DataCSV")
            if not os.path.exists(csv_data_path):
                os.mkdir(csv_data_path)
                print("Directory '% s' created" % csv_data_path)
            else:
                all_csv = os.listdir(csv_data_path)
                for file in all_csv:
                    if file.endswith(".csv"):
                        file_path = os.path.join(csv_data_path, file)
                        os.remove(file_path)
                        print(f'remove csv >>>{file_path}')
            IsLastCol_Literal = True
            if IsLastCol_Literal:
                self.digest_csv(filepath, csv_data_path, 3)
            else:
                self.digest_xlsx()

            # df_result.to_csv(f'weight{window}.csv', sep=',')
        except Exception as e:
            raise "grr_data_digest NG >>>" + str(e.args)
        # return df_spec_array  # str(df.shape)
        # return count_total_csv

    def digest_csv(self, *args):
        csv_path, csv_data_path, weighted = args
        """
        weighted average by rolling function
        """
        # arr_lst = []
        mockup_col_name = []
        nest_lst = []
        try:
            df = pd.read_csv(f'{csv_path}', header=0, index_col=0)
            mockup_col_name = df.columns[1:-1]
            df_values = df.iloc[2: df.shape[0], 1: df.shape[1] - 1]  # all values
            for w in range(weighted):
                nest_lst = []
                for col in range(df_values.shape[1]):  # for row in range(loop_row):  # dut_test_times per dut = 9     loop_row = df.shape[0] - 3
                    arr_weight = df_values.iloc[:, col].rolling(w + 2, min_periods=w + 1, center=True).mean().values
                    # nest_lst.append(arr_weight)
                    nest_lst.append(arr_weight)
                csv_file_name = f'GRR{w + 1}.csv'
                csv_path_ = os.path.join(csv_data_path, csv_file_name)
                # flat_lst = [item for sublist in arr_lst for item in sublist]
                flat_lst = [arr for arr in nest_lst]
                df_result = pd.concat([pd.DataFrame(arr) for arr in flat_lst], axis=1)  # df_result = pd.merge([pd.DataFrame(arr) for arr in flat_lst], on='left')
                df_result.columns = mockup_col_name
                df_result.to_csv(csv_path_, index=False)
            # print(f'Sheet "{sheet_name}" saved as "{csv_file_name}"')
            # for i in range(df.shape[1] - 1):
            #     select_arr_ith = np.array(df.iloc[:, i + 1]).reshape(10, 9)
            #     df_testItem = pd.DataFrame(select_arr_ith)
            #     df_testItem = df_testItem.T
            #     df_testItem.index = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
            #     df_testItem.columns = [i for i in range(10)]
            #     grr_data = pd.DataFrame(df_testItem.values.reshape(3, 10, 3))
            #     grr_data.loc['A'].apply(lambda x: x.rolling(window=2).mean())

        except Exception as e:

            raise "xlsx file NG >>>" + str(e.args)

    def digest_xlsx(self, *args):
        source_path, csv_data_path = args
        try:
            # Read all sheets from the Excel file
            xls = pd.ExcelFile(source_path)
            sheet_names = xls.sheet_names
            # Iterate over each sheet and save it as a CSV file
            for idx, sheet_name in enumerate(sheet_names):
                df = pd.read_excel(xls, sheet_name)
                mockup_col_name = df.columns
                csv_file_name = f'GRR{idx + 1}.csv'
                csv_path_ = os.path.join(csv_data_path, csv_file_name)
                df = df.sort_index()
                df.to_csv(csv_path_, index=False)
                print(f'Sheet "{sheet_name}" saved as "{csv_file_name}"')
        except Exception as e:
            raise "xlsx file NG >>>" + str(e.args)

    def grr_summary(self, *args):
        arr_result = []
        path = ""
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(f'%H%M%S')
        try:
            grr_file_path = args
            grr_files = os.listdir(grr_file_path[0])
            for file in grr_files:
                if file.endswith(".csv"):
                    path = os.path.join(grr_file_path[0], file)
                df = pd.read_csv(path, header=0, index_col=0)
                df_select = df.iloc[2:4, 1:]
                df_select = df_select.T
                df_select.columns = df_select.iloc[0]
                df_select.drop(df_select.index[0])
                arr_result.append(df_select)

            df_result = pd.concat([pd.DataFrame(arr) for arr in arr_result], axis=1)
            df_result = df_result.sort_index(axis=1, ascending=False)  # reverse sorting
            _filename = os.path.join(grr_file_path[0], f'Summary_GRR_{formatted_time}.csv')
            df_result.to_csv(_filename, sep=',')

        except Exception as e:
            raise "grr_summary NG >>> " + str(e.args)
        return ""

    def grr_selection(self, *args):
        avg_result_lst = []
        grr_result_lst = []
        # path = ""
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(f'%H%M%S')
        df_result = pd.DataFrame()
        try:
            summary_file_path = args[0]
            grr_csv_gather = os.listdir(summary_file_path)
            for file in grr_csv_gather:
                if file.startswith("Summary"):
                    p = os.path.join(summary_file_path, file)
                    df_result = pd.read_csv(p, header=0, index_col=0)
            # origin_col_name = df_result.columns
            df_result.columns = [i for i in range(df_result.shape[1])]
            df_result = df_result.drop(df_result.index[0])  # delete first redundant row
            for index, row in df_result.iterrows():
                _selected_weigh = row.iloc[-1]
                grr_result_lst.append(row.iloc[int(_selected_weigh)])
                # avg_result_lst.append(row.iloc[int(_selected_weigh) + 4])
            df_result['Final_GRR'] = grr_result_lst
            # df_result['Final_AVG'] = avg_result_lst
            _filename = os.path.join(summary_file_path, f'GRR_Result_{formatted_time}.csv')
            # df_result.columns = origin_col_name
            df_result.to_csv(_filename, sep=',')
            # XlsxManager.highlight_NG(df_result)

        except Exception as e:
            raise "grr_selection NG >>> " + str(e.args)
        return ""

    def convertToDf(*args) -> pd.DataFrame():
        delimiters = ('\t', ',')
        output_rows = []
        record = []
        output_file = 'output.csv'
        lines = args[0].strip().split('\n')
        try:
            for line in lines:
                line = line.strip()
                if not line:
                    continue

                if line[0].isdigit():
                    if record:
                        output_rows.append(record)

                    record = []

                elements = [line]
                for delimiter in delimiters:
                    if delimiter in line:
                        elements = line.split(delimiter)
                        break

                # Add the elements to record
                record.extend(elements)
            if record:
                output_rows.append(record)

            df = pd.DataFrame(output_rows)
            return df
        except Exception as ee:
            raise "convertToDf Err" + str(ee.args)

    # region    Corresponding Tx, Rx, Beam test items
    """
    Tx          --->    ( 7 ~ 14 + 36 ~ 65 ) makeTxTable
    Rx          --->    ( 15 ~ 26 + 66 ~ 105 ) makeRxTable
    BeamForm    --->    ( 105 ~ 109 ) makeBeamFormTable
    """

    def makeTxTable(sourcePath):
        filepath = os.path.join(sourcePath, f'RawData.csv')
        df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
        subset1 = df.loc[7:14]
        subset2 = df.loc[34:65]
        Tx_rows = pd.concat([subset1, subset2])
        # Tx_rows = df.loc[7:14].append(df.loc[34:65])
        Tx_rows = Tx_rows.reset_index(drop=True)
        columnNames = {"0": 'TestItem', "1": 'Frequency', "2": 'DataRate', "3": 'Bandwidth', "4": 'Antenna',
                       "5": 'TxPower',
                       "6": 'Power',
                       "7": 'MaskMargin', "8": 'Freq1', "9": 'Freq2', "10": 'Freq3', "11": 'Freq4', "12": 'Freq5',
                       "13": 'Freq6',
                       "14": 'Freq7', "15": 'Freq8', "16": 'EVM', "17": 'FreqErr', "18": 'SpectrumMask',
                       "19": 'TestTime'}
        Tx_rows = Tx_rows.rename(columns=columnNames)
        TxDf = Tx_rows.iloc[:, 0:21]
        # TxTable = pd.DataFrame()
        # TxDf['TestItem'] = TxDf['TestItem']
        TxDf['Frequency'] = TxDf['Frequency'].str.split("Frequency: ").str[1]
        TxDf['DataRate'] = TxDf['DataRate'].str.split("Data Rate: ").str[1]
        TxDf['Bandwidth'] = TxDf['Bandwidth'].str.split("Bandwidth: BW-").str[1]
        TxDf['Antenna'] = TxDf['Antenna'].str.split("Antenna: ANT_").str[1]
        TxDf['TxPower'] = TxDf['TxPower'].str.split("Tx Power: ").str[1]
        TxDf['Power'] = TxDf['Power'].str.split("Power             ").str[1]
        # TxDf['MaskMargin'] = TxDf['MaskMargin']
        TxDf['Freq1'] = TxDf['Freq1'].str.split("Frequency          ").str[1]
        TxDf['Freq2'] = TxDf['Freq2'].str.split("Frequency          ").str[1]
        TxDf['Freq3'] = TxDf['Freq3'].str.split("Frequency          ").str[1]
        TxDf['Freq4'] = TxDf['Freq4'].str.split("Frequency          ").str[1]
        TxDf['Freq5'] = TxDf['Freq5'].str.split("Frequency          ").str[1]
        TxDf['Freq6'] = TxDf['Freq6'].str.split("Frequency          ").str[1]
        TxDf['Freq7'] = TxDf['Freq7'].str.split("Frequency          ").str[1]
        TxDf['Freq8'] = TxDf['Freq8'].str.split("Frequency          ").str[1]
        TxDf['EVM'] = TxDf['EVM'].str.split("EVM          ").str[1]
        TxDf['FreqErr'] = TxDf['FreqErr'].str.split("Freq Error          ").str[1]
        TxDf['SpectrumMask'] = TxDf['SpectrumMask'].str.split("Spectrum Mask   ").str[1]
        TxDf['TestTime'] = TxDf['TestTime'].str.split("Test time: ").str[1]
        # TxDf.head()
        csvpath = os.path.join(sourcePath, "Data")
        TxDf.to_csv(os.path.join(csvpath, f'TxDF.csv'), sep=',', encoding='UTF-8')

    def makeRxTable(sourcePath):
        filepath = os.path.join(sourcePath, f'RawData.csv')
        df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
        subset1 = df.loc[15:26]
        subset2 = df.loc[66:105]
        Rx_rows = pd.concat([subset1, subset2])
        Rx_rows = Rx_rows.reset_index(drop=True)
        columnNames = {"0": 'TestItem', "1": 'Frequency', "2": 'DataRate', "3": 'Bandwidth',
                       "4": 'Antenna', "5": 'RxPower', "6": 'Per', "7": 'TestTime'}

        RxDf = Rx_rows.iloc[:, 0:9]
        RxDf = RxDf.rename(columns=columnNames, inplace=False)
        # RxTable = pd.DataFrame()
        # RxDf['TestItem'] = RxDf['TestItem']
        RxDf['Frequency'] = RxDf['Frequency'].str.split("Frequency: ").str[1]
        RxDf['DataRate'] = RxDf['DataRate'].str.split("Data Rate: ").str[1]
        RxDf['Bandwidth'] = RxDf['Bandwidth'].str.split("Bandwidth: BW-").str[1]
        RxDf['Antenna'] = RxDf['Antenna'].str.split("Antenna: ANT_").str[1]
        RxDf['RxPower'] = RxDf['RxPower'].str.split("Rx Power: ").str[1]
        RxDf['Per'] = RxDf['Per'].str.split("PER    ").str[1]
        RxDf['PER_result'] = RxDf['Per'].str.split("<-- ").str[1]
        RxDf['TestTime'] = RxDf['TestTime'].str.split("Test time: ").str[1]
        csvpath = os.path.join(sourcePath, "Data")
        RxDf.to_csv(os.path.join(csvpath, f'RxDF.csv'), sep=',', encoding='UTF-8')

    def makeBeamFormTable(sourcePath):
        filepath = os.path.join(sourcePath, f'RawData.csv')
        df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
        WifiBeamForming_rows = df.loc[106:109]
        WifiBeamForming_rows = WifiBeamForming_rows.reset_index(drop=True)
        # Create a dictionary to map the old column names to the new column names
        columnNames = {"0": 'TestItem', "1": 'TxFrequency', "2": 'TxDataRate', "3": 'TxBandwidth', "4": 'TxAntenna',
                       "5": 'TxPower', "6": 'RxFrequency', "7": 'RxDataRate', "8": 'RxBandwidth', "9": 'RxAntenna',
                       "10": 'RxPower', "11": 'rPcal', "12": 'rPcal_core3', "13": 'TxBF', "14": 'RxFreq',
                       "15": 'RxDR', "16": 'RxBw', "17": 'RxAnt', "18": 'RxPow', "19": 'TxFreq',
                       "20": 'TxDR', "21": 'TxBw', "22": 'TxAnt', "23": 'TxPow', "24": 'PowerDiff', "25": 'TestTime'}

        WifiBeamForming_rows = WifiBeamForming_rows.rename(columns=columnNames)
        WifiBeamForming_rows = WifiBeamForming_rows.iloc[:, 0:27]
        WifiBeamForming_Table = pd.DataFrame()
        WifiBeamForming_Table['TestItem'] = WifiBeamForming_rows['TestItem']
        WifiBeamForming_Table['TxFrequency'] = WifiBeamForming_rows['TxFrequency'].str.split("Tx Frequency: ").str[1]
        WifiBeamForming_Table['TxDataRate'] = WifiBeamForming_rows['TxDataRate'].str.split("Data Rate: ").str[1]
        WifiBeamForming_Table['TxBandwidth'] = WifiBeamForming_rows['TxBandwidth'].str.split("Bandwidth: ").str[1]
        WifiBeamForming_Table['TxAntenna'] = WifiBeamForming_rows['TxAntenna'].str.split("Antenna: ").str[1]
        WifiBeamForming_Table['TxPower'] = WifiBeamForming_rows['TxPower'].str.split("Tx Power: ").str[1]
        WifiBeamForming_Table['RxFrequency'] = WifiBeamForming_rows['RxFrequency'].str.split("Rx Frequency: ").str[1]
        WifiBeamForming_Table['RxDataRate'] = WifiBeamForming_rows['RxDataRate'].str.split("Data Rate: ").str[1]
        WifiBeamForming_Table['RxBandwidth'] = WifiBeamForming_rows['RxBandwidth'].str.split("Bandwidth: ").str[1]
        WifiBeamForming_Table['RxAntenna'] = WifiBeamForming_rows['RxAntenna'].str.split("Antenna: ").str[1]
        WifiBeamForming_Table['RxPower'] = WifiBeamForming_rows['RxPower'].str.split("Rx Power: ").str[1]
        WifiBeamForming_Table['rPcal'] = WifiBeamForming_rows['rPcal'].str.split("rPcal: ").str[1]
        WifiBeamForming_Table['rPcal_core3'] = WifiBeamForming_rows['rPcal_core3'].str.split("rPcal_core3: ").str[1]
        WifiBeamForming_Table['TxBF'] = WifiBeamForming_rows['TxBF'].str.split("TxBF Cal            ").str[1]
        WifiBeamForming_Table['RxFreq'] = WifiBeamForming_rows['RxFreq'].str.split("Rx Frequency: ").str[1]
        WifiBeamForming_Table['RxDR'] = WifiBeamForming_rows['RxDR'].str.split("Data Rate: ").str[1]
        WifiBeamForming_Table['RxBw'] = WifiBeamForming_rows['RxBw'].str.split("Bandwidth: ").str[1]
        WifiBeamForming_Table['RxAnt'] = WifiBeamForming_rows['RxAnt'].str.split("Antenna: ").str[1]
        WifiBeamForming_Table['RxPow'] = WifiBeamForming_rows['RxPow'].str.split("Rx Power: ").str[1]
        WifiBeamForming_Table['TxFreq'] = WifiBeamForming_rows['TxFreq'].str.split("Tx Frequency: ").str[1]
        WifiBeamForming_Table['TxDR'] = WifiBeamForming_rows['TxDR'].str.split("Data Rate: ").str[1]
        WifiBeamForming_Table['TxBw'] = WifiBeamForming_rows['TxBw'].str.split("Bandwidth: ").str[1]
        WifiBeamForming_Table['TxAnt'] = WifiBeamForming_rows['TxAnt'].str.split("Antenna: ").str[1]
        WifiBeamForming_Table['TxPow'] = WifiBeamForming_rows['TxPow'].str.split("Tx Power: ").str[1]
        WifiBeamForming_Table['PowerDiff'] = WifiBeamForming_rows['PowerDiff'].str.split("Power Diff          ").str[1]
        WifiBeamForming_Table['TestTime'] = WifiBeamForming_rows['TestTime'].str.split("Test time: ").str[1]
        # WifiBeamForming_Table.head()
        csvpath = os.path.join(sourcePath, "Data")
        WifiBeamForming_Table.to_csv(os.path.join(csvpath, f'BeamForming_Table.csv'), sep=',', encoding='UTF-8')

    # endregion

    # region    Corresponding Tx, Rx CALIBRATION items
    """
    Corresponding test items
    {
        5. WIFI_RX_CALIBRATION  ---> makeWifiRxCalib5   ,  
        6. WIFI_TX_CALIBRATION  ---> makeWifiTxCalib6   ,
        32. WIFI_RX_CALIBRATION ---> makeWifiRxCalib32  ,
        33. WIFI_TX_CALIBRATION ---> makeWifiTxCalib33
    }
    """

    def makeWifiTxCalib33(sourcePath):
        """
        # The testItem of 33. WIFI_TX_CALIBRATION as a CSV which contain two tables
          * Calibration TX Power
          * Verify TX Power
        """
        excel_file = 'WIFI_TX_CALIBRATION33.xlsx'
        dfsCalfTXPow = pd.DataFrame()
        dfsVerfTXPow = pd.DataFrame()
        filepath = os.path.join(sourcePath, f'RawData.csv')
        xlsxPath = os.path.join(os.path.join(sourcePath, "Data"), f'{excel_file}')
        try:
            df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
            row33 = df.loc[33].transpose().dropna().reset_index(drop=True)
            # row33 = row33[not row33.str.contains("-----------")].reset_index(drop=True)
            CalibrationTXPower = row33.loc[5:72]
            VerifyTXPower = row33.loc[76:144]
            dfsCalfTXPow[['Rate', 'Ant', 'Target', 'Actual', 'Diff']] = CalibrationTXPower.iloc[:].str.split('\s+',
                                                                                                             expand=True)
            dfsVerfTXPow[['Rate', 'Ant', 'Target', 'Actual']] = VerifyTXPower.iloc[:].str.split('\s+', expand=True)
            dfsCalfTXPow.reset_index(drop=True)
            dfsVerfTXPow.reset_index(drop=True)
            dfsCalfTXPow.loc[25:, ['Actual', 'Diff']] = dfsCalfTXPow.loc[25:, ['Diff', 'Actual']].values
            with pd.ExcelWriter(xlsxPath, engine='openpyxl') as writer:
                dfsCalfTXPow.to_excel(writer, sheet_name='CalibrationTXPower', index=False)
                dfsVerfTXPow.to_excel(writer, sheet_name='VerifyTXPower', index=False)
        except SyntaxError as synEx:
            raise "err! " + str(synEx.args)
        except Exception as ee:
            raise f"make Tx Calif excel in valid\n" + str(ee.args)

    def makeWifiTxCalib6(sourcePath):
        """
        # The testItem of 6. WIFI_TX_CALIBRATION as a xlsx which contain two excel table sheets
          * Calibration TX Power
          * Verify TX Power
        """
        excel_file = 'WIFI_TX_CALIBRATION6.xlsx'
        dfs6Calf = pd.DataFrame()
        dfs6Verf = pd.DataFrame()
        filepath = os.path.join(sourcePath, f'RawData.csv')
        xlsxPath = os.path.join(os.path.join(sourcePath, "Data"), f'{excel_file}')
        try:
            df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
            row6 = df.loc[6].transpose().dropna().reset_index(drop=True)
            # row6 = row6[~row6.str.contains("-----------")].reset_index(drop=True)
            CalibTXPower = row6.loc[5:16]
            VerifyTXPower = row6.loc[20:31]
            dfs6Calf[['Rate', 'Ant', 'Target', 'Actual', 'Diff']] = CalibTXPower.iloc[:].str.split('\s+', expand=True)
            dfs6Verf[['Rate', 'Ant', 'Target', 'Actual']] = VerifyTXPower.iloc[:].str.split('\s+', expand=True)
            dfs6Calf.reset_index(drop=True)
            dfs6Verf.reset_index(drop=True)
            dfs6Calf.loc[9:, ['Actual', 'Diff']] = dfs6Calf.loc[9:, ['Diff', 'Actual']].values
            with pd.ExcelWriter(xlsxPath, engine='openpyxl') as writer:
                dfs6Calf.to_excel(writer, sheet_name='CalibrationTXPower', index=False)
                dfs6Verf.to_excel(writer, sheet_name='VerifyTXPower', index=False)

        except SyntaxError as synEx:
            raise "err! " + str(synEx.args)
        except Exception as ee:
            raise f"make Tx Calif excel in valid\n" + str(ee.args)

    def makeWifiRxCalib5(sourcePath):
        """
        # 5. WIFI_RX_CALIBRATION as a csv
          * Calibration TX Power
          * Verify TX Power
        """
        filepath = os.path.join(sourcePath, f'RawData.csv')
        try:
            df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
            WIFI_RX_CALIBRATION = df.loc[5].transpose().dropna().reset_index(drop=True)
            # selectHeader = WIFI_RX_CALIBRATION.loc[0:1].reset_index(drop=True)
            lastIndex = WIFI_RX_CALIBRATION.index[-1]
            selectFront = WIFI_RX_CALIBRATION.loc[2:5]
            selectBack = WIFI_RX_CALIBRATION.loc[7:10]
            selectTestTime = WIFI_RX_CALIBRATION.loc[lastIndex:]
            itemsFront = selectFront.iloc[:].str.split(":", expand=True)
            itemsFront[1] = itemsFront[1].apply(lambda s: s.split())
            itemsBack = selectBack.iloc[:].str.split(":", expand=True).reset_index(drop=True)
            itemsTestTime = selectTestTime.iloc[:].str.split(":", expand=True).reset_index(drop=True)
            itemsBack.loc[1:, [1, 0]] = itemsBack.loc[1:, [0, 1]].values
            itemsBack[1].loc[0] = itemsBack[1].agg(lambda x: x.tolist())
            itemsBack = itemsBack.loc[[0]].reset_index(drop=True)
            result = pd.concat([itemsFront, itemsBack, itemsTestTime])  # selectHeader
            result.columns = ['keys', 'values']
            result.reset_index(drop=True)
            # print(result)
            csvpath = os.path.join(sourcePath, "Data")
            result.to_csv(os.path.join(csvpath, f'WIFI_RX_CALIBRATION_5.csv'), sep=',', encoding='UTF-8')
        except Exception as ee:
            raise f"make Tx Calif5 excel in valid\n" + str(ee.args)

    def selectRow(rowRange: list, filterData, isSplit: bool):
        selected_rows = pd.Series(False, index=filterData.index)
        result = None
        for start, end in rowRange:
            selected_rows[start:end] = True
        selected = filterData[selected_rows]
        if isSplit:
            rowValues = selected.iloc[:].str.split(":", expand=True)
            rowValues[1] = rowValues[1].apply(lambda s: s.split())
            print(rowValues)
            return rowValues
        else:
            result = selected.iloc[:].str.split(":", expand=True).reset_index(drop=True)
            row_ranges = [(1, 3), (5, 7), (9, 11)]
            last_row_range = (13, None)
            # exchanges ------------
            for start, end in row_ranges:
                result.loc[start:end, [1, 0]] = result.loc[start:end, [0, 1]].values
            result.loc[last_row_range[0]:, [1, 0]] = result.loc[last_row_range[0]:, [0, 1]].values
            # exchanges ------------
            row_ranges = [(0, 3), (4, 7), (8, 11)]
            last_row_range = (12, None)
            # melting to combine
            for i, (start, end) in enumerate(row_ranges):
                result[1].loc[i * 4] = result[1].loc[start:end].agg(lambda x: x.tolist())

            result[1].loc[12] = result[1].loc[last_row_range[0]:].agg(lambda x: x.tolist())
            result = result.loc[[0, 4, 8, 12]].reset_index(drop=True)
            result = result.reset_index(drop=True)
            return result

    def makeWifiRxCalib32(sourcePath):
        """
        # 32. WIFI_RX_CALIBRATION as a csv
          * Calibration TX Power
          * Verify TX Power
        """
        filepath = os.path.join(sourcePath, f'RawData.csv')
        try:
            df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
            WIFI_RX_CALIBRATION = df.loc[32].transpose().dropna().reset_index(drop=True)
            data = WIFI_RX_CALIBRATION.loc[1:52]
            filterData = data[~data.str.contains("-----------|========")].reset_index(drop=True)
            row_ranges = [(1, 7), (12, 18), (23, 26), (31, 37)]
            row_FinalGainErr = [(8, 12), (19, 23), (27, 31), (38, 42)]
            lastIndex = WIFI_RX_CALIBRATION.index[-1]
            selectTestTime = WIFI_RX_CALIBRATION.loc[lastIndex:]  # .loc[[-1]].reset_index(drop=True)
            itemsFront = Digest_utils.selectRow(rowRange=row_ranges, filterData=filterData, isSplit=True)
            itemsBack = Digest_utils.selectRow(rowRange=row_FinalGainErr, filterData=filterData, isSplit=False)

            itemsTestTime = selectTestTime.iloc[:].str.split(":", expand=True).reset_index(drop=True)
            result = pd.concat([itemsFront, itemsBack, itemsTestTime])  # selectHeader
            result.columns = ['keys', 'values']
            csvpath = os.path.join(sourcePath, "Data")
            result.reset_index(drop=True)
            result.to_csv(os.path.join(csvpath, f'WIFI_RX_CALIBRATION_32.csv'), sep=',', encoding='UTF-8')
        except Exception as ee:
            raise f"make Tx Calif32 excel in valid\n" + str(ee.args)

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

    def NG_Open_log_txt(self, directory_path, output_csv_path):
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        ending_keyword = "END MARKED"
        USL_lst = []
        LSL_lst = []
        testItem_lst = []
        pattern = r"~"
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
                            if ending_keyword in line:  # stop reading til the end keyword
                                break
                            # Find the indices of the keywords in the line
                            index1 = line.find(keyword1)
                            index2 = line.find(keyword2)
                            test_item_name = line[:index1].strip(' ').split(' ')[-1]
                            testItem_lst.append(test_item_name)
                            specRange = line[index1 + len(keyword1):index2].strip()
                            if not re.search(pattern, specRange):
                                USL_lst.append("PASS")
                                LSL_lst.append("PASS")
                            else:
                                LSL_lst.append(specRange.split('~')[0])
                                USL_lst.append(specRange.split('~')[1])
                                # Write the file name and line to the CSV file
                                # csv_writer.writerow([file_name, f'{line.strip()}']
            # file.close()
            txtFile.close()
            return LSL_lst, USL_lst, testItem_lst
        except UnicodeDecodeError:
            print(f"Error decoding file {txtFile}. Skipping...")
            raise "UnicodeDecodeError"
        except io.UnsupportedOperation:
            print("not readable")
            raise "io exception"
        except Exception as e:
            raise "digestFiles$NG >>> " + str(e.args)

    def Open_log_txt(self, file_path, output_csv_path):
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        flag = False
        USL_lst = []
        LSL_lst = []
        testItem_lst = []
        countStressTimes = 0
        pattern = r"~"
        ending_keyword = "END MARKED"
        IsAllcollected = False
        try:
            with open(output_csv_path, 'w', newline='', encoding='utf-16') as txtFile:
                # csv_writer = csv.writer(csvfile)
                if os.path.isfile(file_path):
                    with open(file_path, 'r', encoding='utf-16') as file:
                        for line_number, line in enumerate(file, start=1):
                            if ending_keyword in line:  # stop reading til the end keyword
                                countStressTimes += 1
                                flag = True
                            if keyword1 in line and keyword2 in line:
                            # Find the indices of the keywords in the line
                                index1 = line.find(keyword1)
                                index2 = line.find(keyword2)
                                if not flag:
                                    test_item_name = line[:index1].strip(' ').split(' ')[-1]
                                    testItem_lst.append(test_item_name)
                                # specRange = line[index1 + len(keyword1):index2].strip()
                                # if not re.search(pattern, specRange):
                                #     USL_lst.append("PASS")
                                #     LSL_lst.append("PASS")
                                # else:
                                #     LSL_lst.append(specRange.split('~')[0])
                                #     USL_lst.append(specRange.split('~')[1])
                                txtFile.write(f'{line.strip()}\n')
                            # Write the file name and line to the CSV file
                            # csv_writer.writerow([file_name, f'{line.strip()}'])
        except UnicodeDecodeError:
            print(f"Error decoding file {file}. Skipping...")
        except Exception as e:
            raise "digestFiles$NG >>> " + str(e.args)
        print("----------------")
        # print(countStressTimes)
        return len(testItem_lst)
        # return LSL_lst, USL_lst, testItem_lst

    def txt_rush(self, file_path):
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        ending_keyword = "END MARKED"
        USL_lst = []
        LSL_lst = []
        testItem_lst = []
        pattern = r"~"
        try:
            with open(file_path, mode='r', encoding='utf-16', errors='ignore') as file:
                lines = file.readlines()
                for line in lines:
                    if ending_keyword in line:  # stop reading til the end keyword
                        break
                    # Find the indices of the keywords in the line
                    index1 = line.find(keyword1)
                    index2 = line.find(keyword2)
                    test_item_name = line[:index1].strip(' ').split(' ')[-1]
                    testItem_lst.append(test_item_name)
                    specRange = line[index1 + len(keyword1):index2].strip()
                    if not re.search(pattern, specRange):
                        USL_lst.append("PASS")
                        LSL_lst.append("PASS")
                    else:
                        LSL_lst.append(specRange.split('~')[0])
                        USL_lst.append(specRange.split('~')[1])
            file.close()
            if len(testItem_lst) == 5810:
                print(len(testItem_lst))
            return LSL_lst, USL_lst, testItem_lst
        except Exception as e:
            raise "Open txt NG >>> " + str(e.args)

    def washing(self, file_path, countTestItems):
        """
        Diagnosis >>> count test items
        :return:
        """
        # file_path = "C:\\Users\\23002496\\PycharmProjects\\DigestATSuite\\IMQX.csv"
        keyword1 = "SPEC:"
        keyword2 = "Value:"
        proj_name = "SIMPLE.txt"
        specRange = ""
        pattern = r"~"
        testItem_values = ""
        all_lst = []
        USL_lst = []
        LSL_lst = []
        data_lst = []
        testItem_lst = []
        # countTestItems = 5810
        IsSpecRange_ready = False
        # file_path = os.path.join(file_path, proj_name)
        # countStressTimes = 10  # num_lst = 0
        try:
            # self.Open_log_txt()
            with open(file_path, mode='r', encoding='utf-16', errors='ignore') as file:
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
                        # countTestItems = len(USL_lst)
                        all_lst.append(data_lst)
                        data_lst = []
                self.pack_result(all_lst, LSL_lst, USL_lst, testItem_lst)
                # df = pd.DataFrame(np.array(all_lst))
                # df.index = (df.index[0:] + 2).tolist()
                # df.loc[0] = pd.Series(LSL_lst)  # insert SPEC
                # df.loc[1] = pd.Series(USL_lst)  # insert SPEC
                # df = df.sort_index()
                # df.columns = pd.Series(testItem_lst)  # insert test item name
                # df = df.T
                # df.insert(loc=2, column='AVG', value="")  # df['avg'] = ""
                # df.insert(loc=3, column='STD', value="")
                # df.insert(loc=4, column='CPK', value="")
                # df.rename(columns={0: 'LSL'}, inplace=True)
                # df.rename(columns={1: 'USL'}, inplace=True)
                # df.reset_index()
                # writer = pd.ExcelWriter('trySample.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'strings_to_numbers': True}})
                # # Convert the dataframe to an XlsxWriter Excel object.
                # df.to_excel(writer, sheet_name='Sheet1')
                # XlsxManager.cooking_CPK(None, writer=writer, shape=df.shape)
            file.close()
            # return all_lst

        except Exception as e:
            raise "washing$NG >>> " + str(e.args)

    def pack_result(self, result_list, LSL_lst, USL_lst, testItem_lst):
        try:
            # LSL_lst, USL_lst, testItem_lst = self.txt_rush()
            df = pd.DataFrame(np.array(result_list))
            df.index = (df.index[0:] + 2).tolist()
            df.loc[0] = pd.Series(LSL_lst)  # insert SPEC
            df.loc[1] = pd.Series(USL_lst)  # insert SPEC
            df = df.sort_index()
            df.columns = pd.Series(testItem_lst)  # insert test item name
            df = df.T
            df.insert(loc=2, column='AVG', value="")  # df['avg'] = ""
            df.insert(loc=3, column='STD', value="")
            df.insert(loc=4, column='CPK', value="")
            df.rename(columns={0: 'LSL'}, inplace=True)
            df.rename(columns={1: 'USL'}, inplace=True)
            df.reset_index()
            writer = pd.ExcelWriter('trySample.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'strings_to_numbers': True}})
            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name='Sheet1')
            XlsxManager.cooking_CPK(None, writer=writer, shape=df.shape)
            # df.to_csv("IMQX_sample.csv", sep=',')
        except Exception as e:
            raise "pack_result$NG >>> " + str(e.args)
