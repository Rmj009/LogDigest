import os
import openpyxl
import csv
import pandas as pd


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

            # Add the elements to the current record
            record.extend(elements)
        if record:
            output_rows.append(record)

        df = pd.DataFrame(output_rows)
        return df
    except Exception as ee:
        raise "convertToDf Err" + str(ee.args)


def makeTxTable(sourcePath):
    filepath = os.path.join(sourcePath, f'RawData.csv')
    df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
    subset1 = df.loc[7:14]
    subset2 = df.loc[34:65]
    Tx_rows = pd.concat([subset1, subset2])
    # Tx_rows = df.loc[7:14].append(df.loc[34:65])
    Tx_rows = Tx_rows.reset_index(drop=True)
    columnNames = {"0": 'TestItem', "1": 'Frequency', "2": 'DataRate', "3": 'Bandwidth', "4": 'Antenna', "5": 'TxPower',
                   "6": 'Power',
                   "7": 'MaskMargin', "8": 'Freq1', "9": 'Freq2', "10": 'Freq3', "11": 'Freq4', "12": 'Freq5',
                   "13": 'Freq6',
                   "14": 'Freq7', "15": 'Freq8', "16": 'EVM', "17": 'FreqErr', "18": 'SpectrumMask', "19": 'TestTime'}
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
    # wifiTxCalif=pd.DataFrame(WifiTxCALIBRATION)
    # def extract_first_literal(string):
    #     return string.strip('[]').split('\t')
    # # wifiTxCalif.columns
    # data = CalibrationTXPower.apply(lambda s: "\t".join(s.strip('[]').split()))
    try:
        df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
        row33 = df.loc[33].transpose().dropna().reset_index(drop=True)
        # row33 = row33[not row33.str.contains("-----------")].reset_index(drop=True)
        CalibrationTXPower = row33.loc[5:71]
        VerifyTXPower = row33.loc[76:144]
        dfsCalfTXPow[['Rate', 'Ant', 'Target', 'Actual', 'Diff']] = CalibrationTXPower.iloc[:].str.split('\s+',
                                                                                                         expand=True)
        dfsVerfTXPow[['Rate', 'Ant', 'Target', 'Actual']] = VerifyTXPower.iloc[:].str.split('\s+', expand=True)
        dfsCalfTXPow.reset_index(drop=True)
        dfsVerfTXPow.reset_index(drop=True)
        dfsCalfTXPow.loc[20:, ['Actual', 'Diff']] = dfsCalfTXPow.loc[20:, ['Diff', 'Actual']].values
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
        CalibTXPower = row6.loc[5:15]
        VerifyTXPower = row6.loc[20:30]
        dfs6Calf[['Rate', 'Ant', 'Target', 'Actual', 'Diff']] = CalibTXPower.iloc[:].str.split('\s+', expand=True)
        dfs6Verf[['Rate', 'Ant', 'Target', 'Actual']] = VerifyTXPower.iloc[:].str.split('\s+', expand=True)
        dfs6Calf.reset_index(drop=True)
        dfs6Verf.reset_index(drop=True)
        dfs6Calf.loc[5:, ['Actual', 'Diff']] = dfs6Calf.loc[5:, ['Diff', 'Actual']].values
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
    dfs5 = pd.DataFrame()
    try:
        df = pd.read_csv(filepath, header=0, sep=',', encoding='UTF-8')
        WIFI_RX_CALIBRATION = df.loc[5].transpose().dropna().reset_index(drop=True)
        # dfs5['Rx_Gain_Err'] = WIFI_RX_CALIBRATION.loc[2].split("Rx Gain Err: ")[-1]
        # dfs5['RSSI'] = WIFI_RX_CALIBRATION.loc[3].split("RSSI: ")[0]
        # dfs5['Diff_value'] = WIFI_RX_CALIBRATION.loc[4].split("Diff value:  ")[0]
        # split_data = WIFI_RX_CALIBRATION.str.split('\n ')
        series_data = WIFI_RX_CALIBRATION.loc[3:5]
        keys = series_data.str.split(':').str[0].str.strip()
        values = series_data.str.split(':').str[1].str.strip()
        aaa = values.str.split('  ', expand=True)
        remainFailGainErr = WIFI_RX_CALIBRATION.loc[6:9]
        # aaa = data.iloc[:].str.split('\s+', expand=True)

    except Exception as ee:
        raise f"make Tx Calif excel in valid\n" + str(ee.args)


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
        dfs32 = pd.DataFrame()
        # split_data = WIFI_RX_CALIBRATION.str.split('\n ')
        data = WIFI_RX_CALIBRATION.loc[1:51]
        # remainFailGainErr = WIFI_RX_CALIBRATION.loc[[7, 8, 9]]
        filterData = data[~data.str.contains("-----------|========")].reset_index(drop=True)
        # filter
        row_ranges = [(0, 6), (11, 17), (22, 25), (33, 36)]
        selected_rows = pd.Series()

        for start, end in row_ranges:
            selected_rows = selected_rows.append(filterData.loc[start:end])

        aaa = selected_rows.iloc[:].str.split('\s+', expand=True)
    except Exception as ee:
        raise f"make Tx Calif excel in valid\n" + str(ee.args)
