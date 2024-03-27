from tkinter import ttk, filedialog, messagebox
# from DigestData import PreManifest, DataUtils
from my_utils import Digest_utils
from info_Manager import *
import tkinter as tk
# import glob
import os


class StartPage(object):
    global project_name

    def __init__(self, master, **kwargs):
        title = kwargs.pop('title')
        self.master = master
        # super().__init__()
        self.windows = []
        self.GGR_option = 0
        self.font = ('Times New Roman', 9, "bold")
        self.path = os.path.dirname(os.path.abspath('__file__'))
        # master.iconbitmap(os.path.join(self.path, "_wnc.ico"))
        self.frame = tk.Frame(master, bg='gray66', width=100, height=160)
        self.frame.grid(row=0, column=0, padx=10, pady=5)
        self.txt = tk.Text(master, font=self.font, width=200, height=150, wrap=tk.WORD)
        label = tk.Label(self.frame, text=title)
        label.grid(row=0, column=0, padx=10, pady=5)
        # label.pack(side="top", fill=tk.BOTH, pady=10)
        self.label = tk.Label(self.frame, font=self.font, text="Keyword: END MARKED", justify='left')
        # self.label.pack(side='top', padx=5, pady=5)

        # self.combo = ttk.Combobox(self.frame, state="readonly", values=["GGR1", "GGR2", "GGR3", "GGR4", "GGR5"])
        # self.btnPages = tk.Button(self.frame, text="open pages", command=lambda: self.create_frames())
        self.btnOpen = tk.Button(self.frame, text="Open", command=lambda: self.open_grr_file())
        self.btnOpenLog = tk.Button(self.frame, text="Open", command=lambda: threading.Thread(target=self.open_log_txt()))
        # self.btnSummaryGRR = tk.Button(self.frame, text="GRR Summary", command=lambda: self.summary_grr())
        # self.btnConcludeGRR = tk.Button(self.frame, text="GRR Conclusion", command=lambda: self.final_grr())
        self.btnGrrCalc = tk.Button(self.frame, text="GRR Calculation", command=lambda: threading.Thread(target=self.Clone_Weight_Data()))
        self.btnSchewart = tk.Button(self.frame, text="Diagram", command=lambda: self.CpkChart_schewart())
        # Combobox creation
        n = tk.StringVar(self.frame, "1")
        values = {"GRR": "1",
                  "GRR weight": "5"}

        # ggr_lst = ttk.Combobox(self.frame, width=27, textvariable=n)
        # ggr_lst['values'] = ('GGR1', 'GGR2', 'GGR3', 'GGR4', 'GGR5')
        # self.combo.bind("<<ComboboxSelected>>", self.handle_selection(event=self.btnGrrCalc.config(state=tk.ACTIVE)))
        # self.combo.set("GRR1")
        # self.combo.place(x=5, y=5)
        # self.btnOpen.grid(row=1, column=0, padx=10, pady=10, rowspan=True)
        self.btnOpenLog.grid(row=2, column=0, padx=10, pady=10, rowspan=True, columnspan=3)
        # self.combo.pack(side='top', padx=5, pady=5, anchor="w")
        # tk.Label(self.frame, text="What is your favorite car barnd?").grid(row=0, column=0, columnspan=3, pady=10, padx=10)
        # for (text, value) in values.items():
        # tk.Checkbutton(self.frame, text="weight GGR1~GRR5", command=lambda: threading.Thread(target=self.Clone_Weight_Data())).grid(row=3, column=0, padx=10, pady=10, rowspan=1)

        self.btnGrrCalc.grid(row=5, column=0, padx=10, pady=10, rowspan=True)
        self.btnSchewart.grid(row=6, column=0, padx=10, pady=10, rowspan=True)
        # self.btnSummaryGRR.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnConcludeGRR.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnPages.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiTx = tk.Button(self.frame, text="Yield WIFI_TX_table", command=lambda: self.ReadRawData("Tx"))

        # self.btnReadWifiRx = tk.Button(self.frame, text="Yield WIFI_RX_table", command=lambda: self.ReadRawData("Rx"))
        # self.btnReadWifiBeam = tk.Button(self.frame, text="Yield WIFI_Beam_table",
        #                                  command=lambda: self.ReadRawData("BeamForm"))

        # self.btnClean = tk.Button(self.frame, text="Clean Data", command=lambda: self.ReadRawData(""))
        # self.btnReadTxCalf33 = tk.Button(self.frame, text="Yield Tx Calibration 33",
        #                                  command=lambda: self.ReadRawData("TxCalf33"))
        # self.btnReadTxCalf6 = tk.Button(self.frame, text="Yield Tx Calibration 6",
        # self.btnReadRxCalf32 = tk.Button(self.frame, text="Yield Rx Calibration 32",
        #                                  command=lambda: self.ReadRawData("RxCalf32"))
        # self.btnReadRxCalf5 = tk.Button(self.frame, text="Yield Rx Calibration 5",
        #                                 command=lambda: self.ReadRawData("RxCalf5"))

        # self.btnReadWifiTx.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiRx.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiBeam.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnClean.pack(side='top', padx=10, pady=5)
        # self.btnReadTxCalf33.pack(side='top', padx=10, pady=5, anchor="w")
        #                                 command=lambda: self.ReadRawData("TxCalf6"))
        # self.btnReadTxCalf6.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadRxCalf32.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadRxCalf5.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnExit = tk.Button(self.frame, text="Close", command=lambda: master.quit())
        self.btnExit.grid(row=20, column=0, padx=10, pady=10, rowspan=True)
        # self.btnSummaryGRR.config(state=tk.DISABLED)
        # self.btnConcludeGRR.config(state=tk.DISABLED)
        # self.combo.config(state=tk.DISABLED)
        # self.btnReadWifiTx.config(state=tk.DISABLED)
        # self.btnReadWifiRx.config(state=tk.DISABLED)
        # self.btnReadWifiBeam.config(state=tk.DISABLED)
        # self.btnReadTxCalf33.config(state=tk.DISABLED)
        # self.btnReadTxCalf6.config(state=tk.DISABLED)
        # self.btnReadRxCalf32.config(state=tk.DISABLED)
        # self.btnReadRxCalf5.config(state=tk.DISABLED)
        # self.btnPages.config(state=tk.DISABLED)
        # self.btnGrrCalc.config(state=tk.DISABLED)
        # self.txt_widget = scrolledtext.ScrolledText(self.frameTxt, font=self.font, wrap=tk.WORD)
        # self.txt_widget.pack(expand=True, fill='both')

        self.create_dataDir()
        # self.show_frame(StartPage)

        # print(info_manager.get_info('------'))
        self.frame.pack(side='left', fill=tk.BOTH, expand=False)
        self.txt.pack(side='left')
        self.txt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
        self.grr_filePath: str = ""
        self.grr_spec = None
        self.info_manager = InfoManager(self.txt)
        self.util_obj = Digest_utils(self.path)
        self.result_path = os.path.join(self.path, "Result")
        self.Data_logs = os.path.join(self.path, "DataLog")

        # button1 = tk.Button(self, text="Go to Page One", command=lambda: controller.show_frame(PageOne))

    def create_frames(self):
        container = tk.Frame(self.master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # for F in (PageOne, PageTwo):
        #     frame = F(container, self.root)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def final_grr(self):
        try:
            self.util_obj.grr_selection(self.result_path)
            self.info_manager.update_info("GRR Conclusion", f'{self.result_path}')
        except Exception as e:
            messagebox.showerror("Conclude GRR NG", "Plz make sure index at last column and retry")
            raise "summary_grr NG >>> " + str(e.args)

    def summary_grr(self):
        try:
            self.util_obj.grr_summary(self.result_path)
            self.info_manager.update_info("GRR Summary", f'{self.result_path}')
            # self.btnConcludeGRR.config(state=tk.ACTIVE)
        except Exception as e:
            messagebox.showerror("Summary NG", "Plz retry")
            raise "summary_grr NG >>> " + str(e.args)

    def calc_grr(self, df):  # , avg_weigh):
        try:
            self.util_obj.grr_roasting(df, avg_weigh=3)
            """
            GRR for multiple averaging for vertical data display
            """
            # csv_path_select = os.path.join(csv_data_path, f'{csv}')
            # grr_csv_ = os.listdir(csv_data_path)
            # for avg_weigh, csv in enumerate(grr_csv_):
            #     self.util_obj.grr_cooking(self.path, csv_path_select, avg_weigh)
            #     csv_path_select = os.path.join(csv_data_path, f'{csv}')
            #
            # self.info_manager.update_info("Gage R&R Calculation", f'{self.result_path}')
            # self.btnSummaryGRR.config(state=tk.ACTIVE)
        except Exception as e:
            print("calculate GRR err >>> " + str(e.args))
            messagebox.showerror("Xlsx File might open!", "Plz close xlsx & try again")
            # raise "calculate GRR err >>> " + str(e.args)

    def Clone_Weight_Data(self):
        # Sort the files based on modification time (newest first)
        try:
            files = os.listdir(self.result_path)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.result_path, x)), reverse=True)
            result_xlsx_filename = os.path.join(self.result_path, files[0])
            self.util_obj.digest_xlsx(result_xlsx_filename)
            self.info_manager.update_info("clone via weight", f'{self.result_path}')
            # self.btnConcludeGRR.config(state=tk.ACTIVE)
        except Exception as e:
            messagebox.showerror("Clone_Weight_Data$NG", "Plz retry")
            raise "Clone_Weight_Data$NG >>> " + str(e.args)

    def CpkChart_schewart(self):
        try:
            diagram_folder = os.path.join(self.path, "Diagram")
            os.mkdir(diagram_folder) if not os.path.exists(diagram_folder) else None
            files = os.listdir(self.result_path)
            files.sort(key=lambda x: os.path.getmtime(os.path.join(self.result_path, x)), reverse=True)
            lates_xlsx_file = os.path.join(self.result_path, files[0])
            self.util_obj._plt_chart(lates_xlsx_file, 2)
            self.info_manager.update_info("Plotting CPK", f'show Diagram in {diagram_folder}')
        except Exception as e:
            messagebox.showerror("Clone_Weight_Data$NG", "Plz retry")
            raise "Clone_Weight_Data$NG >>> " + str(e.args)

    def open_log_txt(self):
        global grr_lst
        proj = "IMQX"
        projName_file = f'{proj}.csv'
        countTestItems = 0
        countStressTime = 0
        df_info = (countTestItems, countStressTime)
        global origin_log_fileName
        try:
            if not os.path.exists(self.Data_logs):
                os.mkdir(self.Data_logs)
            if not os.path.exists(self.result_path):
                os.mkdir(self.result_path)
            if logPath := filedialog.askopenfilename(title='Select Files', filetypes=[('Text files', '*.txt'), ('All files', '*.*')]):
                # os.path.isfile(logPath)
                self.info_manager.start_info_manager_thread()
                df_info = self.util_obj.Open_log_txt(logPath, os.path.join(self.Data_logs, projName_file))
                files = os.listdir(self.Data_logs)
                # Sort the files based on modification time (newest first)
                files.sort(key=lambda x: os.path.getmtime(os.path.join(self.Data_logs, x)), reverse=True)
                origin_log_fileName = os.path.splitext(os.path.basename(logPath))[0]
                Read1st_path = os.path.join(self.Data_logs, files[0])
                # df, num_NG = self.util_obj.washing(read_parse_fileName, df_info, origin_log_fileName)
                all_lst, LSL_lst, USL_lst = self.util_obj.washing(Read1st_path, df_info)
                # ----- chk num of data before acquire GRR column -----
                df = self.util_obj.pack_result(all_lst, LSL_lst, USL_lst, origin_log_fileName)
                if df.shape[1] > 90:
                    # self.calc_grr(df=df)  # , avg_weigh=3)
                    # self.btnGrrCalc.config(state=tk.ACTIVE)
                    # self.combo.config(state=tk.ACTIVE)
                    grr_lst = self.util_obj.grr_roasting(df)
                    self.util_obj.grr_packingXlsx(grr_lst, 3)
                    self.info_manager.update_info(f'Open log {logPath}',
                                                  f'Test_Items: {df_info[1]}'
                                                  f'    PASS: {(df.shape[1] - 5)}')  # NG:{num_NG}
                else:
                    self.info_manager.update_info(f'Open log {logPath}',
                                                  f'Test Items: {df_info[1]}     PASS: {(df.shape[1] - 5)} '  # NG:{num_NG}
                                                  f'\r\n  StressTest under 90,  cannot run GRR')
            else:
                self.info_manager.update_info("Open NG", "Didn't select file")
        except IOError as ioe:

            messagebox.showerror("Xlsx File might open!", "Plz close xlsx & try again")
        except Exception as e:
            messagebox.showerror("FILE_ERR", "Invalid data log or EngMode data, Plz reload file")
            raise "log file NG >>> " + str(e.args)

    def open_grr_file(self):
        try:
            # y_or_n = messagebox.askquestion("Question", "Weighted Average by users")  if y_or_n == 'yes': # yes,  no
            # self.grr_filePath = filedialog.askopenfilename(filetypes=[("Xlsx files", "*.xlsx")])
            self.grr_filePath = filedialog.askopenfilename()
            if self.grr_filePath:
                # self.info_manager.start_info_manager_thread()
                count_csv = 3
                self.util_obj.grr_data_digest(self.grr_filePath)
                g_file = [f'GRR{i + 1},' for i in range(int(count_csv))]
                self.info_manager.update_info("Open .xlsx average by users", f'File Path {self.grr_filePath}')
                self.info_manager.update_info("Open .xlsx and create .csv", "csv  ".join(g_file) + ".csv")
                # self.btnGrrCalc.config(state=tk.ACTIVE)
                self.combo.config(state=tk.ACTIVE)
            else:
                messagebox.showerror("No FILE", "Plz reload file")
                return False
        except Exception as e:
            messagebox.showerror("FILE_ERR", "Plz reload file")
            raise "open grr file NG >>> " + str(e.args)
        return True

    def handle_selection(self, event=None):
        selected_option = self.combo.get()
        print("Selected option:", selected_option)
        self.GGR_option = selected_option

    def choose_file(self):
        filePath = filedialog.askopenfilename()
        self.info_manager.update_info(f'Loading from file path', filePath)
        if filePath:
            try:
                with open(filePath, 'r') as file:
                    content = file.read()
                    df = Digest_utils.convertToDf(content)
                    df.to_csv(os.path.join(self.path, f'RawData.csv'), sep=',', encoding='UTF-8')
                    self.info_manager.update_info(f'Save Raw DataFrame in the Data Folder', "OK")
                    self.btnReadWifiTx.config(state=tk.ACTIVE)
                    self.btnReadWifiRx.config(state=tk.ACTIVE)
                    self.btnReadWifiBeam.config(state=tk.ACTIVE)
                    self.btnReadTxCalf6.config(state=tk.ACTIVE)
                    self.btnReadTxCalf33.config(state=tk.ACTIVE)
                    self.btnReadRxCalf32.config(state=tk.ACTIVE)
                    self.btnReadRxCalf5.config(state=tk.ACTIVE)

            except Exception as ex:
                messagebox.showerror("Loading Err!", "File not exist or Invalid File")
                raise "open txt failure => " + str(ex.args)
        return

    def create_dataDir(self) -> object:
        dirs_to_create = ['Data']
        for dir_name in dirs_to_create:
            dir_path = os.path.join(self.path, dir_name)
            os.makedirs(dir_path, exist_ok=True)

    def ReadRawData(self, *args):
        table_mapping = {
            "Rx": {"func": Digest_utils.makeRxTable, "message": "WifiRx"},
            "Tx": {"func": Digest_utils.makeTxTable, "message": "WifiTx"},
            "BeamForm": {"func": Digest_utils.makeBeamFormTable, "message": "Wifi_BeamForm"},
            "TxCalf33": {"func": Digest_utils.makeWifiTxCalib33, "message": "Wifi Tx Calib33"},
            "TxCalf6": {"func": Digest_utils.makeWifiTxCalib6, "message": "Wifi Tx Calib6"},
            "RxCalf32": {"func": Digest_utils.makeWifiRxCalib32, "message": "Wifi Tx RxCalf32"},
            "RxCalf5": {"func": Digest_utils.makeWifiRxCalib5, "message": "Wifi Tx RxCalf5"}
        }

        if args[0] in table_mapping:
            table_info = table_mapping[args[0]]
            table_info["func"](self.path)
            self.info_manager.update_info("Succeed", f'Save {table_info["message"]} Table in the Data Folder')
        else:
            messagebox.showerror("Loading Err!", "File not exist or Invalid File")
            raise ValueError(f"Invalid argument: {args[0]}")

    def run(self):
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.master.mainloop()

    def on_exit(self):  # obj: object
        # loop through all windows and destroy them
        for window in self.windows:
            window.destroy()
        self.master.grab_set()  # .grab_release()
        self.master.destroy()

    def number_to_string(self, argument):
        match argument:
            case 0:
                return "zero"
            case 1:
                return "one"
            case 2:
                return "two"
            case default:
                return "something"

    # def removeDir(self):
    #     self.info_manager.update_info(" Clear Data in directory ", " Empty Data")
    #     try:
    #         for path in [self.DirDataSketch, self.DirDataPolish, self.DirDataRx, self.DirData]:
    #             DestroyData.DestroyDirectory(path)
    #     except FileExistsError as fileErr:
    #         raise "remove Err === " + str(fileErr.args)
    #     except Exception as eee:
    #         raise f'remove ERR' + str(eee.args)

    # def ReadRawData(self, *args):
    #     try:
    #         # ---------------- Tx, Rx, BeamFrom Tables ----------------------
    #         if args[0] == "Rx":
    #             utils.makeRxTable(self.path)
    #             self.info_manager.update_info("Succeed", f'Save WifiRx Table in the Data Folder')
    #         elif args[0] == "Tx":
    #             utils.makeTxTable(self.path)
    #             self.info_manager.update_info("Succeed", f'Save WifiTx Table in the Data Folder')
    #         elif args[0] == "BeamForm":
    #             utils.makeBeamFormTable(self.path)
    #             self.info_manager.update_info("Succeed", f'Save Wifi_BeamForm Table in the Data Folder')
    #         # -------------------Tx Calibration-------------------------
    #         elif args[0] == "TxCalf33":
    #             utils.makeWifiTxCalib33(self.path)
    #             self.info_manager.update_info("Succeed", f'Save Wifi Tx Calib33 Table in the Data Folder')
    #         elif args[0] == "TxCalf6":
    #             utils.makeWifiTxCalib6(self.path)
    #             self.info_manager.update_info("Succeed", f'Save Wifi Tx Calib6 Table in the Data Folder')
    #         # -------------------Rx Calibration-------------------------
    #         elif args[0] == "RxCalf32":
    #             utils.makeWifiRxCalib32(self.path)
    #             self.info_manager.update_info("Succeed", f'Save Wifi Tx RxCalf32 Table in the Data Folder')
    #         elif args[0] == "RxCalf5":
    #             utils.makeWifiRxCalib5(self.path)
    #             self.info_manager.update_info("Succeed", f'Save Wifi Tx RxCalf5 Table in the Data Folder')
    #     except Exception as ex:
    #         messagebox.showerror("Loading Err!", "File not exist or Invalid File")
    #         raise "open txt failure => " + str(ex.args)

    # def DestroyDirectory(path: str):
    #     files = glob.glob(f'{path}/*')
    #     for f in files:
    #         os.remove(f)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.root = tk.Tk()
        self.root.title("PageOne")
        label = tk.Label(self, text="This is Page One")
        label.pack(side="top", fill="x", pady=10)
        # button1 = tk.Button(self, text="Go to Start Page",
        #                     command=lambda: controller.show_frame())
        # button1.pack()
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.root = tk.Tk()
        self.root.title("PageTwo")
        label = tk.Label(self, text="This is Page Two")
        label.pack(side="top", fill="x", pady=10)
        # button1 = tk.Button(self, text="Go to Start Page",
        #                     command=lambda: controller.show_frame(StartPage))
        # button1.pack()
        button2 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global countTestItems
    global info_manager
    root = tk.Tk()
    frame_size = "600x400"
    root.geometry(frame_size)
    root.winfo_toplevel().title("< NPI_Analysis_Tool >")
    app = StartPage(root, title="GRR analysis")
    app.run()
