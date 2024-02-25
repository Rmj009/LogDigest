import datetime
import os
import numpy as np
import pandas as pd
from Gage import Gage


# import openpyxl


class Digest_utils:
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
            grr_value = grr_instance.rawData_handling(grr_data)
        except Exception as e:
            raise "grr_calculation" + str(e.args)
        return grr_value

    def grr_cooking(filepath: str, grr_spec):
        """
        split dataframe into A,B,C blocks
        :return:
        """
        grr_lst = ["0"]  # ["GRR"]
        current_time = datetime.datetime.now()
        formatted_time = current_time.strftime(f'%m%d_%H%M%S')
        try:
            df = pd.read_csv(f'{filepath}', skiprows=4, header=None, index_col=0)
            df = df.iloc[:, :-1]  # ignore last column

            for i in range(df.shape[1] - 1):
                select_arr_ith = np.array(df.iloc[:, i + 1]).reshape(10, 9)
                grr_lst.append(Digest_utils.grr_calculation(select_arr_ith, grr_spec[:, i]))
            df_result = pd.read_csv(f'{filepath}', header=0, index_col=0)
            df_result = df_result.iloc[:, :-1]
            grr_lst = [np.nan if val == '0' else float(val) for val in grr_lst]
            df_result.loc['GRR'] = np.array(grr_lst)

            df_result = pd.DataFrame(df_result)
            df_result.to_csv(f'GGR__{formatted_time}.csv', sep=',')
            # df_result = pd.concat([df.iloc[:3], result, df.iloc[3:]]).reset_index(drop=True)

        except Exception as e:
            raise "grr_cooking" + str(e.args)
        return "success"

    def grr_data_digest(self: str) -> np.array:
        window = 2
        arr_weight = pd.DataFrame()
        arr_result = pd.DataFrame()
        df_result = pd.DataFrame()  # index=range(df.shape[0]), columns=range(df.shape[1])
        arr_lst = []

        try:
            df = pd.read_csv(f'{self}', header=0, index_col=0)
            df = df.iloc[:, :-1]  # ignore last column
            loop_row_time = df.shape[0] // 9
            df_spec_array = df.iloc[[0, 1]].values[:, 1:]

            df_values = df.iloc[3: df.shape[0], 1: df.shape[1]]  # all values
            for col in range(df_values.shape[1]):
                nest_lst = []
                for row in range(loop_row_time):  # dut_test_times per dut = 9
                    arr_weight = pd.DataFrame(df_values.iloc[:9 * (row + 1), col])  # slice by _dut
                    arr_weight = np.array(
                        arr_weight.rolling(window, min_periods=(window // 2), center=True).mean().values)
                    nest_lst.append(arr_weight)
                    # arr = np.random.rand(3, 1)
                    # nest_lst.append(arr)
                    # arr_result = np.append(arr_result, arr_weight)
                # df_result[f'{col}'] = arr_weight.tolist()
                arr_lst.append(nest_lst)
            flat_lst = [item for sublist in arr_lst for item in sublist]
            df_result = pd.concat([pd.DataFrame(arr) for arr in flat_lst], axis=1)
            # df_result = pd.merge([pd.DataFrame(arr) for arr in flat_lst])
            print(df_result)

            # for i in range(df.shape[1] - 1):
            #     select_arr_ith = np.array(df.iloc[:, i + 1]).reshape(10, 9)
            #     df_testItem = pd.DataFrame(select_arr_ith)
            #     df_testItem = df_testItem.T
            #     df_testItem.index = ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C']
            #     df_testItem.columns = [i for i in range(10)]
            #     grr_data = pd.DataFrame(df_testItem.values.reshape(3, 10, 3))
            #     grr_data.loc['A'].apply(lambda x: x.rolling(window=2).mean())

            # /////////////////////////////////////////////////////////////////////
            # for col_nth in df.columns:
            #     mv2df[col_nth] = df[col_nth].rolling(window=2).mean()
            # range_specLst = df_spec_array[0] - df_spec_array[1]
            # print("Columns in the DataFrame:")
            # for column in df.columns:
            #     print(column)
            # print("\nLooping through the data in each column:")
            # for column in df.columns:
            #     print(f"Column: {column}")
            #     for value in df[column]:
            #         print(value)
            df_result.to_csv(f'weight{window}.csv', sep=',')
        except Exception as e:
            raise "csv data under 90" + str(e.args)
        return df_spec_array  # str(df.shape)

    def cooking_moving_average(cols):
        try:
            mv_arr = cols
        except Exception as e:
            raise "_moving_average" + "NG >>>" + str(e.args)
        return mv_arr  # str(df.shape)

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