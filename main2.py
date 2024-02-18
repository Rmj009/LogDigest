import os
import json
import tkinter as tk

import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from collections import namedtuple
from matplotlib.figure import Figure
from tkinter import filedialog, ttk, messagebox
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import AseTreeMap
# import DestroyData
from mainViz import RfVisualize
from DigestData import PreManifest, DataUtils
from abc import ABCMeta, abstractmethod

CSVFile = namedtuple('CSVFile', ['filename', 'path'])


class AbcAseAz(metaclass=ABCMeta):

    def __init__(self):
        pass

    def __getitem__(self, index):
        pass
        # return self.csv_files[index].path


class InfoManager:
    def __init__(self, txt_widget):
        self.font = ('Times New Roman', 12, "bold")
        self.txt_widget = txt_widget
        self.info = {}

    def update_info(self, title, info):
        self.info[title] = info
        self.update_text_widget()
        # ConfigTxt = tk.Text(self.frame, font=self.font, width=80, height=60, bg='white', fg='black')
        # ConfigTxt.insert(tk.END, f'{configFile} \n')

    def get_info(self, title):
        return self.info.get(title, "")

    def update_text_widget(self):
        self.txt_widget.config(state=tk.NORMAL)
        self.txt_widget.delete('1.0', tk.END)
        for title, info in self.info.items():
            self.txt_widget.insert(tk.END,
                                   f"{title}\n----------------------\n"
                                   f"{info}\r\n ======================================================= \r\n")
            self.txt_widget.see('end')
        self.txt_widget.config(state=tk.DISABLED)


class SimDcApp(AbcAseAz):

    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.geometry("750x600")
        self.root.title("SIMDC inside project")
        self.frame = tk.Frame(self.root, bg='gray78', width=100, height=160)
        self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        self.frame.pack(side='left', fill=tk.BOTH, expand=True)
        # self.frameFig = tk.Frame(self.root, width=300, height=500, bg='white')
        # self.frameFig.grid(row=0, column=1, padx=10, pady=10, sticky='ne')
        self.font = ('Times New Roman', 12, "bold")
        self.label = tk.Label(self.frame, font=('Times', 20, 'bold underline'), text="Descriptive Spectrum",
                              bg='azure3',
                              justify='left')
        self.label.pack(side='top', padx=5, pady=5)
        self.simDC_menubar()
        self.txt = tk.Text(self.frame, font=self.font, width=80, height=60, wrap=tk.WORD)
        self.txt.pack(side='left')
        self.txt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
        self.info_manager = InfoManager(self.txt)
        self.fig = None
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.windows = []
        # self.directory = directory
        self.rootDir = os.path.dirname(os.path.abspath("main.py"))
        self.create_dataDir()
        self.DirData = os.path.join(self.rootDir, 'Data')
        self.DirDataPolish = os.path.join(self.rootDir, 'DataPolish')
        self.DirDataSketch = os.path.join(self.rootDir, 'DataSketch')
        self.DirDataRx = os.path.join(self.rootDir, 'DataRx')
        self.graphFig = os.path.join(self.rootDir, 'graphFig')
        self.File = namedtuple('File', ['filename', 'path'])
        self.files = [CSVFile(filename=f, path=self.DirData) for f in os.listdir(self.DirData) if f.endswith('.csv')]
        self.filelist = [self.File(filename=file, path=self.DirData) for file in self.files]
        # Add a scrollbar to the Text widget
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.txt.yview)
        scrollbar.pack(side='right', fill='y')
        self.txt['yscrollcommand'] = scrollbar.set

    def __len__(self):
        return len(self.filelist)

    def __getitem__(self, index):
        return self.filelist[index]

    def update_canvas(self, canvas):
        # if hasattr(self, "canvas_widget"):
        #     self.canvas_widget.destroy()
        if hasattr(self, 'canvas'):  # check if self.canvas exists
            self.canvas.get_tk_widget().pack_forget()  # remove prior canvas from self.frame
        self.canvas = canvas  # store the new canvas object in self.canvas
        self.canvas.draw_idle()
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

    def create_dataDir(self):
        dirs_to_create = ['DataPolish', 'DataSketch', 'Data', 'DataRx', 'graphFig']
        for dir_name in dirs_to_create:
            dir_path = os.path.join(self.rootDir, dir_name)
            os.makedirs(dir_path, exist_ok=True)

    def manifest_csv(self, *args) -> list[str]:
        csvList = []
        my_dict = {}
        csvPath = os.path.join(self.rootDir, str(args[0]))
        files = [CSVFile(filename=f, path=csvPath) for f in os.listdir(csvPath) if f.endswith('.csv')]
        try:
            for filename, filePath in enumerate(files):
                if filename is not None:
                    csvList.append(files[filename][0])
                    # self.txt.insert(tk.END, f'{files[filename][0]} \n')
                else:
                    csvList = None
                    return csvList
        except Exception as acqEE:
            raise str(acqEE.args)
        for i, val in enumerate(csvList, start=1):
            my_dict[f'Item {i}'] = val
        data = json.dumps(my_dict, sort_keys=True, indent=2)
        self.info_manager.update_info(f'{args[0]} contain data: ', data)
        return csvList

    def disable_menu(self, menu):
        for item in menu.winfo_children():
            if isinstance(item, tk.Menu):
                self.disable_menu(item)
            else:
                item.entryconfig(0, state=tk.DISABLED)

    def simDC_menubar(self):
        menuBar = tk.Menu(self.root)
        # create the file menu and add it to the menu bar
        syncDBMenu = tk.Menu(menuBar, tearoff=0)
        syncDBMenu.add_command(label="Connect to DataBase", command=lambda: self.ConnectForm())
        syncDBMenu.add_command(label="Disconnect", command=lambda: None)
        syncDBMenu.add_separator()
        syncDBMenu.add_command(label="Drop", command=lambda: None)
        menuBar.add_cascade(label="Sync", menu=syncDBMenu)

        # create the file menu and add it to the menu bar
        fileMenu = tk.Menu(menuBar, tearoff=0)
        fileMenu.add_command(label="Open", command=lambda: self.open_file())
        fileMenu.add_command(label="Write Config", command=lambda: self.fillForm())
        fileMenu.add_separator()
        fileMenu.add_command(label="Remove All data", command=lambda: self.removeDir())
        menuBar.add_cascade(label="File", menu=fileMenu)

        # create the Query menu and add it to the menu bar
        # global fillWindow
        logQueryMenu = tk.Menu(menuBar, tearoff=0)
        logQueryMenu.add_command(label="Pass", command=lambda: self.identifyResult("Pass"))
        logQueryMenu.add_command(label="Fail", command=lambda: self.identifyResult("Fail"))
        logQueryMenu.add_command(label="Water Request", command=lambda: self.identifyResult("water"))
        menuBar.add_cascade(label="Query", menu=logQueryMenu)

        # create the Monitor menu and add it to the menu bar
        monitorMenu = tk.Menu(menuBar, tearoff=0)
        monitorMenu.add_command(label="Power Over SPEC", command=lambda: self.overSPEC("Power"))
        monitorMenu.add_command(label="EVM Over SPEC", command=lambda: self.overSPEC("EVM"))
        monitorMenu.add_command(label="PowerCpk", command=lambda: self.monitorCPK("Power"))
        monitorMenu.add_command(label="EvmCpk", command=lambda: self.monitorCPK("EVM"))
        menuBar.add_cascade(label="Monitor", menu=monitorMenu)

        # create the Monitor menu and add it to the menu bar
        DiagramMenu = tk.Menu(menuBar, tearoff=0)
        DiagramMenu.add_command(label="Custom RidgeLine", command=lambda: self.ridgeLineSNS())
        DiagramMenu.add_command(label="All RidgeLine", command=lambda: self.ridgeWindow())
        DiagramMenu.add_command(label="Comparison RidgeLine", command=lambda: self.ComparisonType())
        DiagramMenu.add_command(label="Rx TreeMap", command=lambda: self.treemapDiagram(None))
        DiagramMenu.add_command(label="Histogram", command=lambda: None)
        menuBar.add_cascade(label="Diagrams", menu=DiagramMenu)

        ExitMenu = tk.Menu(menuBar, tearoff=0)
        ExitMenu.add_command(label="Exit and Close window", command=self.root.quit)
        menuBar.add_cascade(label="Exit", menu=ExitMenu)
        self.disable_menu(menuBar)
        self.root.config(menu=menuBar)

    def ConnectForm(self, *args):
        """
        Tiangolo SQLModel included
        """
        try:
            syncForm = tk.Toplevel(self.root)
            syncForm.title("Selector panel")
            syncForm.geometry("280x480")
            save_button = tk.Button(syncForm, text="Save", command=lambda: SyncPostgres())
            save_button.pack(side='top', padx=10, pady=5)

            def SyncPostgres():
                result = None
                try:
                    self.info_manager.update_info("儲存configFile.json", result)
                    # ConfigTxt.grid(row=2, column=1)  # self.txt.pack(fill='both', expand=True)
                    # ConfigTxt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
                except Exception as SyncPostgresErr:
                    raise "SyncPostgres" + str(SyncPostgresErr.args)
                finally:
                    pass
                    # TODO: release db
        except Exception as e:
            raise f"Sync Err" + str(e.args)

    def fillForm(self):
        filesInData = self.manifest_csv('Data')
        if filesInData is None:
            messagebox.showerror("File not exist", "No data involved")
            return "Empty"
        else:
            self.info_manager.update_info("From the DataDir", "select the latest")
            self.selectorPanel(filesInData, self.DirData)

    def selectorPanel(self, *args):
        """
        Acquire the latest csv to identify the requirement params whether in Data or DataPolish
        Because the csv is assumed to be homogeneity in the params
        """
        global OptionArr, fillWindow
        fileList = args[0]
        fileDir = args[1]
        filesList = sorted([f for f in fileList if f.endswith("WifiData.csv")])
        csv_files = sorted(filesList, key=lambda x: os.path.getmtime(os.path.join(fileDir, x)))
        filePath = os.path.join(fileDir, csv_files[-1])
        OptionArr = PreManifest().manifestData(filePath)
        try:
            fillWindow = tk.Toplevel(self.root)
            fillWindow.title("Selector panel")
            fillWindow.geometry(
                "280x480+{}+{}".format(int(self.root.winfo_screenwidth() / 2 - 150),
                                       int(self.root.winfo_screenheight() / 2 - 100)))
            # selectOption = tk.StringVar(value="False")
            # Option1 = tk.Radiobutton(fillWindow, text="All Data", variable=selectOption, value=True)
            # Option2 = tk.Radiobutton(fillWindow, text="selected", variable=selectOption, value=False)
            # Option1.pack(side='top', padx=3, pady=3, fill='x')
            # Option2.pack(side='top', padx=3, pady=3, fill='y')
            # ----------------------------------------------------------------------------
            # # add some widgets and Create and position the combo box
            # fileListLabel = tk.Label(fillWindow, text="Files")
            # fileListLabel.pack()
            # comboxFileList = ttk.Combobox(fillWindow, values=fileList)
            # comboxFileList.pack(side='top', padx=6, pady=5, fill='both')
            # ----------------------------------------------------------------------------
            # filePath = os.path.join(self.DirDataPolish, comboxFileList.get())
            # print(repr(ase_preprocess))
            # OptionArr = PreManifest().manifestData(filePath)
            moduleLabel = tk.Label(fillWindow, text="Wifi Modules")
            moduleLabel.pack()
            comboxType = ttk.Combobox(fillWindow, values=OptionArr[0])
            # selected_comboxType.set("A")  # set the default selection
            comboxType.pack(side='top', padx=6, pady=5, fill='both')
            antLabel = tk.Label(fillWindow, text="Antenna")
            antLabel.pack()
            comboxAnt = ttk.Combobox(fillWindow, values=OptionArr[1])
            comboxAnt.pack(side='top', padx=6, pady=5, fill='both')
            bwLabel = tk.Label(fillWindow, text="Bandwidth")
            bwLabel.pack()
            BwCombox = ttk.Combobox(fillWindow, values=OptionArr[2])
            BwCombox.pack(side='top', padx=6, pady=5, fill='both')
            save_button = tk.Button(fillWindow, text="Save", command=lambda: save_option())
            save_button.pack(side='top', padx=10, pady=5)

            def save_option():
                wifiType = comboxType.get()
                antenna = comboxAnt.get()
                bw = BwCombox.get()
                if len(wifiType.strip()) == 0:
                    messagebox.showinfo("config File Err", "請選填 Wifi Modules")
                    return None
                elif len(antenna.strip()) == 0:
                    messagebox.showinfo("config File Err", "請選填 Antenna")
                    return None
                elif len(bw.strip()) == 0:
                    messagebox.showinfo("config File Err", "請選填 Bandwidth")
                    return None
                file_path = os.path.join(self.rootDir, "configFile.json")
                try:
                    if fileDir == self.DirDataPolish:
                        DataUtils.processingCsvAll(wifiType, self.DirDataPolish, self.DirDataSketch, self.DirDataRx)
                    elif fileDir == self.DirData:
                        DataUtils.processingCsv(wifiType, filePath, self.DirDataSketch, self.DirDataRx)
                    configFile = {"WifiType": wifiType, "Antenna": antenna, "BW": bw}
                    with open(file_path, "w") as f:
                        json.dump(configFile, f)
                    data = json.loads(json.dumps(configFile))
                    json_str = json.dumps(data, sort_keys=True, indent=2)
                    self.info_manager.update_info("儲存configFile.json", json_str)
                    # ConfigTxt.grid(row=2, column=1)  # self.txt.pack(fill='both', expand=True)
                    # ConfigTxt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
                except Exception as saveErr:
                    raise "save_option" + str(saveErr.args)
                finally:
                    save_button.config(state=tk.DISABLED)

        except TypeError as csvErr:
            print(f'csvFilesNotExist: {csvErr}')
            messagebox.showerror(str(csvErr), "CSV 不在DataPolish資料夾")
            fillWindow.destroy()
        except Exception as e:
            messagebox.showerror("不明錯誤", "CANNOT refresh form")
            fillWindow.destroy()
            raise "fillForm Err" + str(e.args)

    def identifyResult(self, *args):
        title = f'Show {args[0]} Statistics'
        try:
            if args[0] == "water":
                self.waterTable(args)
                self.info_manager.update_info("title", f'{"result"}')
            else:
                df = self.fileEverExist(self.DirData)
                if messagebox.askyesno("Confirm", "Filter result by config?"):
                    Result = PreManifest.queryResult(df, self.DirData, *args)
                    self.info_manager.update_info(title, f'{Result}')
                # else:
                #     messagebox.showerror("Warning", "請事先載入資料")
        except Exception as ee:
            raise f'overSPEC {str(ee.args)}'
        messagebox.showinfo("Result", f'Show all fail data if config not exist')

    def waterTable(self, *args):
        windowWater = tk.Toplevel(self.root)
        windowWater.title("Miscellaneous query")
        windowWater.geometry("500x420")

        def entry_changed(event):
            entrys = event.widget
            print(entrys.get())

        # mLabel = tk.Label(windowWater, text="Take Option")
        # mLabel.pack()
        # moduleLabel = tk.Label(fillWindow, text="Wifi Modules")
        # moduleLabel.pack()
        filePath = filedialog.askopenfilename()
        OptionArr = PreManifest().manifestData(filePath)
        ArrCol = [[["Wifi Modules"], ["Antenna"]], [["Bandwidth"], ["channel"]]]
        frameWater = tk.Frame(windowWater, borderwidth=1, relief="solid")
        frameWater.grid(row=0, column=0, padx=10, pady=10)

        moduleLabel = tk.Label(frameWater, text="Wifi Modules")

        comboxType = ttk.Combobox(frameWater, values=OptionArr[0])
        antLabel = tk.Label(frameWater, text="Antenna")
        comboxAnt = ttk.Combobox(frameWater, values=OptionArr[1])
        bwLabel = tk.Label(frameWater, text="Bandwidth")
        BwCombox = ttk.Combobox(frameWater, values=OptionArr[2])
        chLabel = tk.Label(frameWater, text="channel")
        comboxCh = ttk.Combobox(frameWater, values=OptionArr[3])

        moduleLabel.pack()
        comboxType.pack(side='top', padx=6, pady=5, fill='both')
        antLabel.pack()
        comboxAnt.pack(side='top', padx=6, pady=5, fill='both')
        bwLabel.pack()
        BwCombox.pack(side='top', padx=6, pady=5, fill='both')
        chLabel.pack()
        comboxCh.pack(side='top', padx=6, pady=5, fill='both')

        save_button = tk.Button(frameWater, text="Save", command=lambda: entry_changed())
        save_button.pack(side='bottom', padx=10, pady=5)

        # ArrCombox = [[[comboxType], [comboxAnt]], [[BwCombox], [ChCombox]]]

        # set column and row weights to distribute space evenly
        # frameWater.grid_columnconfigure(0, weight=1)
        # frameWater.grid_columnconfigure(1, weight=1)
        # frameWater.grid_rowconfigure(0, weight=1)
        # frameWater.grid_rowconfigure(1, weight=1)
        # comboxOptions = [[comboxType, ttk.Label(frameWater, text='Type')], [comboxAnt, ttk.Label(frameWater, text='Ant')]]
        # comboxOptions += [[BwCombox, ttk.Label(frameWater, text='Bandwidth')], [ChCombox, ttk.Label(frameWater, text='Channel')]]

        # sublabel = tk.Label(frameWater, text=f'{ArrCol[0][0]}')
        # sublabel.grid(row=0, column=0, sticky="n")
        # # subentry = ArrCombox[i][j]
        # ArrCombox[0][0][0].grid(row=1, column=1)
        # for i in range(2):
        #     for j in range(2):
        # subentry = comboxOptions[i][j]
        # sublabel = ttk.Label(frameWater, text=f'{comboxOptions[i][j]}:')
        # sublabel.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
        # subentry.grid(row=i + 1, column=j, sticky='nsew', padx=5, pady=5)
        # combox, label = comboxOptions[i * 2 + j]
        # combox.grid(row=i * 2, column=j * 2)
        # label.grid(row=i * 2 + 1, column=j * 2)

        # frameWater.pack()
        # frameWater.grid(row=1, column=1)

        # Create the widgets for each cell
        # label = tk.Label(frame, text=f"Label -----")
        # label.grid(row=0, column=0)
        # entry = tk.Entry(frame)
        # entry.grid(row=0, column=1)

        # Add a sub-grid to the central cell of the main grid
        # subframe = tk.Frame(frame, borderwidth=1, relief="solid")
        # subframe.grid(row=1, column=0, columnspan=2)
        # for i in range(2):
        #     for j in range(2):
        #         subentry = ArrCombox[i][j]
        #         for combo_box in subentry:
        #             sublabel = tk.Label(frameWater, text=f'{ArrCol[i][j]}')
        #             sublabel.grid(row=i*2, column=j*2)
        #             combo_box.grid(row=i*2+1, column=j*2)

        # subentry[i][j].grid(row=i, column=j)

        # for row in range(rows):
        #     for column in range(columns):
        #
        #         waterFrame.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        #
        #         label = tk.Label(windowWater, text=f"Label {row} {column}")
        #         label.grid(row=row, column=column)
        #         entry = tk.Entry(windowWater)
        #         entry.grid(row=row, column=column)
        #         entry.bind("<KeyRelease>", entry_changed)
        #
        # entry2 = tk.Entry(windowWater)
        # entry2.grid(row=1, column=1)

        # # create the label above the text box
        # label = tk.Label(waterFrame, text=f"Cell {i},{j}")
        # label.pack(pady=5)
        #
        # # create the text box
        # textbox = tk.Entry(waterFrame)
        # textbox.pack()
        # button = tk.Button(windowWater, text="Submit")
        # button.grid(row=2, columnspan=2)
        # button.pack(padx=20, pady=10)
        # # add content to the text boxes
        # text_boxes = windowWater.grid_slaves(column=0, row=0)
        # for i, textbox in enumerate(text_boxes):
        #     textbox.insert(0, f"Cell {i},{0}")
        #
        # text_boxes = windowWater.grid_slaves(column=1, row=0)
        # for i, textbox in enumerate(text_boxes):
        #     textbox.insert(0, f"Cell {i},{1}")
        #
        # text_boxes = windowWater.grid_slaves(column=2, row=0)
        # for i, textbox in enumerate(text_boxes):
        #     textbox.insert(0, f"Cell {i},{2}")
        #
        # text_boxes = windowWater.grid_slaves(column=3, row=0)
        # for i, textbox in enumerate(text_boxes):
        #     textbox.insert(0, f"Cell {i},{3}")

        # windowWater.columnconfigure(0, weight=0)
        # windowWater.rowconfigure(0, weight=0)
        return None

    def overSPEC(self, *args):
        try:
            if os.path.exists('configFile.json'):
                selectDf_stat = PreManifest.OverSpec(*args, self.DirDataSketch)
                stats = [selectDf_stat['count'],
                         selectDf_stat['mean'],
                         selectDf_stat['max'],
                         selectDf_stat['min']]
                self.info_manager.update_info(f'{args[0]} OverSpec Statistics', selectDf_stat)

            else:
                self.fileEverExist(self.DirData)
                messagebox.showerror("config檔不存在", "Please replenish selector panel \r\n 請填妥selector panel")
        except Exception as ee:
            raise f'overSPEC {str(ee.args)}'
        # return selectDf_stat

    def monitorCPK(self, *args):
        cpk = 0
        try:
            if os.path.exists('configFile.json'):
                print(f'The {args} csv file exists')
                cpk = DataUtils.peekCpk(*args)
                print('cpk:{0}'.format(cpk))
            else:
                messagebox.showerror("config檔不存在", "Please replenish selector panel \r\n 請填妥selector panel")
        except Exception as ee:
            raise f'overSPEC {str(ee.args)}'
        return cpk

    def open_file(self):
        IsCast = messagebox.askyesno("Confirm", "是否為多筆資料?")
        print(f'Current Pwd: ', {os.path.abspath("")})
        print('------------------------------------------------')
        if IsCast:
            filesPolish = self.manifest_csv('DataPolish')
            if filesPolish is None:
                messagebox.showerror("file not exist", "get no data in DataPolish")
                return None
            else:
                # TODO: divide one by wifiTye for once or all wifiType for once
                messagebox.showinfo("Confirm", "確認資料夾內是否屬於同性質資料")
                """
                heterogeneous data will collapse combination
                """
                askDir = filedialog.askopenfilename()
                wifiType = "11ax"
                dfs = DataUtils.processingCsvAll(wifiType, self.DirDataPolish, self.DirDataSketch, self.DirDataRx)
                # df = PreManifest.RecordFile(None, self.DirData, self.DirDataPolish)
                # csvHeader = PreManifest.fmtPrintHeader(df)
                countDutFail = PreManifest.fmtPrintHeader(dfs)
                self.info_manager.update_info("Dut fail ", countDutFail)
                self.selectorPanel(filesPolish, self.DirDataPolish)
        else:
            oFile_path = filedialog.askopenfilename()
            print(f'FileSourcePath: {0}'.format(oFile_path))
            print('------------------------------------------------')
            # if os.path.isfile(oFile_path):
            if oFile_path:
                try:
                    csvHeader = PreManifest.fmtPrintHeader(oFile_path)
                    self.info_manager.update_info(">>> Loading data ", csvHeader)
                    countDutFail = PreManifest.RecordFile(oFile_path, self.DirData, self.DirDataPolish)
                    self.info_manager.update_info("Which DutNo Fail: ", countDutFail)
                    self.treemapDiagram(oFile_path)
                    # self.frame.pack(side='left')
                    # self.frame.grid_rowconfigure(0, weight=1)
                    # self.frame.grid_columnconfigure(0, weight=1)
                    # self.frame.grid_rowconfigure(1, weight=1)
                    # self.frame.grid_columnconfigure(1, weight=1)
                except Exception as e:
                    raise f'openFile Err->{str(e.args)}'

    def ridgeWindow(self):
        IsSave = messagebox.askyesno("Confirm", "是否儲存所有圖檔?")
        try:
            # file_path = filedialog.asksaveasfilename(
            #     filetypes=(
            #         ("PNG_fig", "*.png"),
            #         ("JPG_fig", "*.jpg")
            #     )
            # )
            RfVisualize.mainViz(IsSave, self.DirDataSketch, self.graphFig)
        except TypeError as csvErr:
            print(f'csvFilesNotExist: {csvErr}')
            messagebox.showerror("csv Err!", "資料格式錯誤或資料不存在")

    def ridgeLineSNS(self):
        try:
            with open('configFile.json', 'r', encoding='UTF-8') as f:
                content = f.read()
            configFile = json.loads(content)
            RfVisualize.ridgeLineSNS(self.DirDataSketch, configFile, self.graphFig)
            RfVisualize.Comparison2(self.DirDataSketch, configFile, self.graphFig)
            self.info_manager.update_info("Plot custom based on configFile.json",
                                          "Save the diagram in graphFig")
        except FileNotFoundError as fe:
            raise f'File not Found' + str(fe.args)
        except Exception as ridgeE:
            raise f'ridgeLineSNS {str(ridgeE.args)}'
        finally:
            pass

    def treemapDiagram(self, *args):
        title = "Plot treemap Diagram"
        sourcePath = args[0]
        try:
            if sourcePath is None:
                IsSave = messagebox.askyesno("Confirm", "是否儲存所有圖檔?")
                if IsSave:
                    messagebox.showinfo("Select file to plot", "Merely accept files in DataRx")
                    # dfRx = self.fileEverExist(self.DirDataRx)
                    dfRx = DataUtils.DigestSketchData(filedialog.askopenfilename())
                    # dfTree = DataUtils.DigestRxTreemap(dfRx)
                    treemapRxFig = AseTreeMap.pltTreeMap(dfRx)
                    canvasRx = FigureCanvasTkAgg(treemapRxFig, master=self.frame)
                    self.update_canvas(canvasRx)
                    # TODO: select specific column to plot Rx
                    # treemapFig = AseTreeMap.AseTreeMap(dfTree)
                    # canvas = FigureCanvasTkAgg(treemapFig, master=self.frame)
                    # self.update_canvas(canvas)
            else:
                dfRx = DataUtils.DigestAskOpenFileName(sourcePath, 1)
                dfTree = DataUtils.DigestTreemap(dfRx)
                treemapFig = AseTreeMap.AseTreeMap(dfTree, IsSave=False)
                canvas = FigureCanvasTkAgg(treemapFig, master=self.frame)
                self.update_canvas(canvas)
        except Exception as TreeErr:
            raise f"treemapDiagram" + str(TreeErr.args)

    def ComparisonType(self):
        global pltBtn
        title = "Do comparison"
        content = "compare two same categorical WifiType with different testing time or motherBoard"
        windowComparison = tk.Toplevel(self.root)
        windowComparison.title(title)
        # Set the window size and position it in the center of the screen
        windowComparison.geometry(
            "280x420+{}+{}".format(int(self.root.winfo_screenwidth() / 2 - 150),
                                   int(self.root.winfo_screenheight() / 2 - 100)))

        # add some widgets and Create and position the combo box
        mLabel = tk.Label(windowComparison, text="Choose csvFile to compare with")
        mLabel.pack()
        try:
            # selected_comboxType.set("A")  # set the default selection
            comboxComparison1 = ttk.Combobox(windowComparison, values=self.manifest_csv('DataSketch'))
            comboxComparison1.pack(padx=10, pady=5)
            comboxComparison2 = ttk.Combobox(windowComparison, values=self.manifest_csv('DataSketch'))
            comboxComparison2.pack(padx=10, pady=5)
            save_button = tk.Button(windowComparison, text="Save", command=lambda: save_csvOption('DataSketch'))
            save_button.pack(padx=20, pady=10)
            # Add a button to close the window
            pltBtn = tk.Button(windowComparison, text="Plot Comparison RidgeLine",
                               command=lambda: ridgeLineComparison())
            pltBtn.pack(padx=20, pady=10)
        except Exception as ComparisonErr:
            raise f'WifiTypeAggregate Err ' + str(ComparisonErr.args)
        finally:
            pltBtn.config(state=tk.DISABLED)

        def save_csvOption(filePath):
            csv1 = comboxComparison1.get()
            csv2 = comboxComparison2.get()
            try:
                if csv1 != csv2:
                    frontPath = os.path.join(self.rootDir, f'{filePath}')
                    csvPath0 = os.path.join(frontPath, f'{csv1}')
                    csvPath1 = os.path.join(frontPath, f'{csv2}')
                    self.info_manager.update_info(title=title, info="Show the diagram \n" + content)
                    result = DataUtils.WifiTypeAggregate(path1=csvPath0, path2=csvPath1, sourcePath=self.DirDataSketch)
                    if result is None:
                        messagebox.showerror("選檔案錯誤", "檔案維度不一致")
                else:
                    self.info_manager.update_info("Comparison Err", info="Duplicated choose!")
                    messagebox.showerror("選檔案錯誤", "請勿選擇相同檔案")
                    raise "User Operation fault"
            except Exception as ee:
                raise "save_csvOption Err" + str(ee.args)
            finally:
                save_button.config(state=tk.DISABLED)
                pltBtn.config(state=tk.ACTIVE)

        def ridgeLineComparison():
            try:
                with open('configFile.json', 'r', encoding='UTF-8') as f:
                    contents = f.read()
                    configFile = json.loads(contents)
                # RfVisualize.ridgeLineSNS(configFile)
                RfVisualize.displayComparison(False, self.DirDataSketch, self.graphFig, configFile)
                self.info_manager.update_info("Plot Comparison ridgeLine",
                                              "Save the diagram in graphFig")
            except Exception as ridgeE:
                raise f'ridgeLineComparison {str(ridgeE.args)}'
            finally:
                save_button.config(state=tk.ACTIVE)
                pltBtn.config(state=tk.DISABLED)

    def fileEverExist(self, *args):
        # TODO: need to debug
        sourcePath = filedialog.askopenfilename()
        givenDir = args[0]
        if sourcePath:
            has_csv = False
            has_xlsx = False
            files = [f for f in os.listdir(givenDir) if f.endswith('.csv')]
            filelist = [CSVFile(filename=f, path=self.DirData) for f in files]
            print(f"Directory contains {0}".format(len(filelist)))
            for filename in os.listdir(givenDir):
                if filename.endswith('.csv'):
                    has_csv = True
                elif filename.endswith('.xlsx'):
                    has_xlsx = True
            return has_xlsx | has_csv
        else:
            if os.path.isfile(sourcePath):
                dfs = DataUtils.DigestAskOpenFileName(sourcePath, 1)
                return dfs

    # def removeDir(self):
    #     self.info_manager.update_info(" Clear Data in directory ",
    #                                   "1. Data \n 2.DataPolish \n 3.DataSketch \n 4.DataRx ")
    #     try:
    #         for path in [self.DirDataSketch, self.DirDataPolish, self.DirDataRx, self.DirData]:
    #             DestroyData.DestroyDirectory(path)
    #     except FileExistsError as fileErr:
    #         raise "remove Err === " + str(fileErr.args)
    #     except Exception as eee:
    #         raise f'remove ERR' + str(eee.args)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.root.mainloop()

    def on_exit(self):  # obj: object
        # loop through all windows and destroy them
        for window in self.windows:
            window.destroy()
        self.root.destroy()


if __name__ == '__main__':
    app = SimDcApp()
    app.run()
    """
        #  protocol statement should be executed before calling
        #  so that the window's "close" button
        #  is properly configured to destroy the window and release resources.
    """

# ref resource : https://stackoverflow.com/questions/52658364/how-to-generate-a-series-of-histograms-on-matplotlib
