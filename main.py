import threading
from tkinter import ttk, filedialog, messagebox, scrolledtext
# from DigestData import PreManifest, DataUtils
from my_utils import Digest_utils
import tkinter as tk
import time
# import glob
import os


class InfoManager:
    def __init__(self, txt_widget):
        self.font = ('Times New Roman', 12, "bold")
        self.txt_widget = txt_widget
        self.info = {}

    def __truediv__(self, other):
        line = "=" * len(other.count)
        return "\n".join([self.txt_widget, line, other.count])

    def update_info(self, title, info):
        self.info[title] = info
        self.update_text_widget()
        # ConfigTxt = tk.Text(self.frame, font=self.font, width=80, height=60, bg='white', fg='black')
        # ConfigTxt.insert(tk.END, f'{configFile} \n')

    def get_info(self, title):
        return self.info.get(title, "")

    def run_info_manager(self):
        global info_manager
        while True:
            # Simulate updating information every 2 seconds
            info_manager.update_info("Time", time.ctime())
            time.sleep(0.5)

    def update_text_widget(self):
        self.txt_widget.config(state=tk.NORMAL)
        self.txt_widget.delete(self.txt_widget, tk.END)
        for title, info in self.info.items():
            self.txt_widget.insert(tk.END, f">>> {title} \n" + ">>> " + f"{info} \r\n")
            self.txt_widget.see('end')
        self.txt_widget.config(state=tk.DISABLED)

    def start_info_manager_thread(self):
        global info_manager_thread
        info_manager_thread = threading.Thread(target=self.run_info_manager)
        info_manager_thread.daemon = True
        info_manager_thread.start()


class StartPage:

    def __init__(self):
        # tk.Tk.__init__(self, *args, **kwargs)
        super().__init__()
        self.root = tk.Tk()
        self.windows = []
        self.GGR_option = 0
        self.root.geometry("750x600")
        self.root.title("Entrance")
        self.font = ('Times New Roman', 12, "bold")
        # self.txt_widget
        self.frame = tk.Frame(self.root, bg='gray66', width=100, height=160)
        self.frame.pack(side='left', fill=tk.BOTH, expand=False)
        # self.frameTxt = tk.Frame(self.root, bg='gray78', width=100, height=160)
        # self.frameTxt.pack(side='right', fill=tk.BOTH, expand=False)

        self.label = tk.Label(self.frame, font=('Times', 20, 'bold'), text="File selection",
                              justify='left')
        self.label.pack(side='top', padx=5, pady=5)
        self.btnOpen = tk.Button(self.frame, text="Open", command=lambda: self.open_grr_file())  # self.chooseFile()
        self.btnOpen.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnGrrCalc = tk.Button(self.frame, text="GRR Calculation",
                                    command=lambda: self.calc_grr())  # self.chooseFile()
        self.combo = ttk.Combobox(self.frame, state="readonly", values=["GGR1", "GGR2", "GGR3", "GGR4", "GGR5"])
        # # label
        # ttk.Label(self.frame, text="Select the Month :",
        #           font=("Times New Roman", 10)).grid(column=0,
        #                                              row=5, padx=10, pady=25)
        # # Combobox creation
        # n = tk.StringVar()
        # ggr_lst = ttk.Combobox(self.frame, width=27, textvariable=n)
        # ggr_lst['values'] = ('GGR1', 'GGR2', 'GGR3', 'GGR4', 'GGR5')
        # self.combo.bind("<<ComboboxSelected>>", self.handle_selection(event=self.btnGrrCalc.config(state=tk.ACTIVE)))
        self.combo.set("GRR1")
        # self.combo.place(x=5, y=5)
        # self.combo.pack(side='top', padx=5, pady=5, anchor="w")
        self.btnGrrCalc.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnSummaryGRR = tk.Button(self.frame, text="Summary GRR", command=lambda: self.summary_grr())
        self.btnSummaryGRR.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnConcludeGRR = tk.Button(self.frame, text="Conclude GRR", command=lambda: self.final_grr())
        self.btnConcludeGRR.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnPages = tk.Button(self.frame, text="open pages", command=lambda: self.create_frames())
        self.btnPages.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiTx = tk.Button(self.frame, text="Yield WIFI_TX_table", command=lambda: self.ReadRawData("Tx"))
        # self.btnReadWifiTx.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiRx = tk.Button(self.frame, text="Yield WIFI_RX_table", command=lambda: self.ReadRawData("Rx"))
        # self.btnReadWifiRx.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiBeam = tk.Button(self.frame, text="Yield WIFI_Beam_table",
        #                                  command=lambda: self.ReadRawData("BeamForm"))
        # self.btnReadWifiBeam.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnClean = tk.Button(self.frame, text="Clean Data", command=lambda: self.ReadRawData(""))
        # self.btnClean.pack(side='top', padx=10, pady=5)
        # self.btnReadTxCalf33 = tk.Button(self.frame, text="Yield Tx Calibration 33",
        #                                  command=lambda: self.ReadRawData("TxCalf33"))
        # self.btnReadTxCalf33.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadTxCalf6 = tk.Button(self.frame, text="Yield Tx Calibration 6",
        #                                 command=lambda: self.ReadRawData("TxCalf6"))
        # self.btnReadTxCalf6.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadRxCalf32 = tk.Button(self.frame, text="Yield Rx Calibration 32",
        #                                  command=lambda: self.ReadRawData("RxCalf32"))
        # self.btnReadRxCalf32.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadRxCalf5 = tk.Button(self.frame, text="Yield Rx Calibration 5",
        #                                 command=lambda: self.ReadRawData("RxCalf5"))
        # self.btnReadRxCalf5.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnExit = tk.Button(self.frame, text="Close Window", command=lambda: self.root.quit())
        self.btnExit.pack(side='bottom', padx=10, pady=5, anchor="sw")
        # self.btnReadWifiTx.config(state=tk.DISABLED)
        # self.btnReadWifiRx.config(state=tk.DISABLED)
        # self.btnReadWifiBeam.config(state=tk.DISABLED)
        # self.btnReadTxCalf33.config(state=tk.DISABLED)
        # self.btnReadTxCalf6.config(state=tk.DISABLED)
        # self.btnReadRxCalf32.config(state=tk.DISABLED)
        # self.btnReadRxCalf5.config(state=tk.DISABLED)
        self.btnPages.config(state=tk.DISABLED)
        self.btnGrrCalc.config(state=tk.DISABLED)
        self.btnSummaryGRR.config(state=tk.DISABLED)
        # self.btnConcludeGRR.config(state=tk.DISABLED)
        self.combo.config(state=tk.DISABLED)
        # self.txt_widget = scrolledtext.ScrolledText(self.frameTxt, font=self.font, wrap=tk.WORD)
        # self.txt_widget.pack(expand=True, fill='both')
        self.txt = tk.Text(self.root, font=self.font, width=200, height=150, wrap=tk.WORD)
        self.txt.pack(side='left')
        self.txt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
        self.path = os.path.dirname(os.path.abspath('__file__'))
        self.create_dataDir()
        self.frames = {}
        # self.show_frame(StartPage)
        self.info_manager = InfoManager(self.txt)

        self.grr_filePath: str = ""
        self.grr_spec = None

        label = tk.Label(self.root, text="This is the Start Page")
        label.pack(side="top", fill="x", pady=10)
        # button1 = tk.Button(self, text="Go to Page One",
        #                     command=lambda: controller.show_frame(PageOne))
        # button1.pack()

    def create_frames(self):
        container = tk.Frame(self.root)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (PageOne, PageTwo):
            frame = F(container, self.root)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def final_grr(self):
        try:
            util_obj = Digest_utils()
            summary_path = os.path.join(self.path, "Summary")
            util_obj.grr_selection(summary_path)
            self.info_manager.update_info("Selection done", f'{summary_path}')
        except Exception as e:
            messagebox.showerror("Conclude GRR NG", "Plz make sure index at last column and retry")
            raise "summary_grr NG >>> " + str(e.args)

    def summary_grr(self):
        try:
            util_obj = Digest_utils()
            summary_path = os.path.join(self.path, "Summary")
            util_obj.grr_summary(summary_path)
            self.info_manager.update_info("Output Summary GRR", f'{summary_path}')
            self.btnConcludeGRR.config(state=tk.ACTIVE)
        except Exception as e:
            messagebox.showerror("Summary NG", "Plz retry")
            raise "summary_grr NG >>> " + str(e.args)

    def calc_grr(self):
        filepath = self.grr_filePath
        try:
            util_obj = Digest_utils()
            # csv_ith = self.combo.get()[3]  # need debug
            csv_data_path = os.path.join(self.path, "DataCSV")
            summary_path = os.path.join(self.path, "Summary")
            if not os.path.exists(summary_path):
                os.mkdir(summary_path)
                print("Directory '% s' created" % summary_path)
            else:
                all_grr_csv = os.listdir(summary_path)
                for file in all_grr_csv:
                    if file.endswith(".csv"):
                        file_path = os.path.join(summary_path, file)
                        os.remove(file_path)
                        print(f'remove csv >>>{file_path}')
            if not os.path.exists(csv_data_path):
                os.mkdir(csv_data_path)
            grr_csv_ = os.listdir(csv_data_path)
            for avg_weigh, csv in enumerate(grr_csv_):
                csv_path_select = os.path.join(csv_data_path, f'{csv}')
                util_obj.grr_cooking(self.path, csv_path_select, avg_weigh)
            # for csv_ith, csv in enumerate(grr_csv_):
            #     csv_path_select = os.path.join(csv_data_path, f'{csv}')

            self.info_manager.update_info("Output Gage R&R csv", f'{summary_path}')
            self.btnSummaryGRR.config(state=tk.ACTIVE)
        except Exception as e:
            raise "calculate GRR err >>> " + str(e.args)

    def open_grr_file(self):
        try:
            self.grr_filePath = filedialog.askopenfilename(filetypes=[("Xlsx files", "*.xlsx")])
            if self.grr_filePath:
                grr_file_path = self.grr_filePath
                self.info_manager.update_info("Read csv OK", f'File Path {self.grr_filePath}')
                count_csv = Digest_utils.grr_data_digest(grr_file_path, self.path)
                g_file = [f'GRR{i + 1},' for i in range(int(count_csv))]
                self.info_manager.update_info("Create .csv", f'{repr(g_file)}.csv')
                self.btnGrrCalc.config(state=tk.ACTIVE)
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

    def create_dataDir(self):
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
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.info_manager.start_info_manager_thread()
        self.root.mainloop()

    def on_exit(self):  # obj: object
        # loop through all windows and destroy them
        for window in self.windows:
            window.destroy()
        self.root.destroy()
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

    app = StartPage()
    txt_widget = scrolledtext.ScrolledText(app.txt, font=('Times New Roman', 12), wrap=tk.WORD)
    txt_widget.pack(expand=True, fill='both')

    info_manager = InfoManager(txt_widget)

    # app.protocol("WM_DELETE_WINDOW", self.on_exit)
    # app.mainloop()
    app.run()
