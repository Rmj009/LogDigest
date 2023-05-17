# WNC homework

## 請針對附件parse出需要的測項資訊, 最後輸出.CSV

* 頻率
* data rate
* bandwidth
* antenna
* target power
* 測試數值


## Execution Steps:

1. 讀取Log File
2. Divide and conquer
    1. 分離測試項目rows與測試條件設定條件項目rows
    2. 分類測試項目出Tx table與Rx table
    
3. 為Tx, Rx, WIFI_IMPLICIT_BEAMFORMING_CAL_VER table 個別建立獨立欄位表格
4. 為儀器初始化條件敘述建立額外table, 獨立Tx\Rx calibration
5. 最後輸出csv or xlsx在Data資料夾中



## 1. Python Environments

### Python版本(詳見Pipfile)

* python_version = "3.10"
* python_full_version = "3.10.6"
` pipenv install --python 3.10.6`


### 2. 安裝相關套件(使用pip或pipenv)
     ` pip install -r requirements.txt` or `pipenv install` 


### 3. 執行專案

`   python3 main.py `