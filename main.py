from tkinter import filedialog, messagebox

from Gage import Gage
from utils import utils
import tkinter as tk
# import glob
import os


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
                                   f"{title}\n ---------------\n"
                                   f"{info}\r\n =========================== \r\n")
            self.txt_widget.see('end')
        self.txt_widget.config(state=tk.DISABLED)


class GUIApp(tk.Tk):

    def __init__(self, *args, **kwargs):

        # super().__init__()
        tk.Tk.__init__(self, *args, **kwargs)

        self.root = tk.Tk()
        self.windows = []
        # self.root.geometry("750x600")
        self.root.title("WNC_")
        self.font = ('Times New Roman', 12, "bold")
        # self.frame = tk.Frame(self.root, bg='gray66', width=100, height=160)
        # # self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        # self.frame.pack(side='left', fill=tk.BOTH, expand=False)
        self.frameTxt = tk.Frame(self.root, bg='gray78', width=100, height=160)
        # # self.frameTxt.grid(row=0, column=1, padx=10, pady=10, sticky='e')
        self.frameTxt.pack(side='right', fill=tk.BOTH, expand=False)

        # self.label = tk.Label(self.frame, font=('Times', 20, 'bold'), text="Load txt before output file!",
        #                       justify='left')
        # self.label.pack(side='top', padx=5, pady=5)
        # self.label.pack(side='top', padx=5, pady=5)
        # self.btnOpen = tk.Button(self.frame, text="Open Txt", command=lambda: self.chooseFile())
        # self.btnOpen.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiTx = tk.Button(self.frame, text="Yield WIFI_TX_table", command=lambda: self.ReadRawData("Tx"))
        # self.btnReadWifiTx.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiRx = tk.Button(self.frame, text="Yield WIFI_RX_table", command=lambda: self.ReadRawData("Rx"))
        # self.btnReadWifiRx.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnReadWifiBeam = tk.Button(self.frame, text="Yield WIFI_Beam_table",
        #                                  command=lambda: self.ReadRawData("BeamForm"))
        # self.btnReadWifiBeam.pack(side='top', padx=10, pady=5, anchor="w")
        # # self.btnClean = tk.Button(self.frame, text="Clean Data", command=lambda: self.ReadRawData(""))
        # # self.btnClean.pack(side='top', padx=10, pady=5)
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
        # self.btnExit = tk.Button(self.frame, text="Close Window", command=lambda: self.root.quit())
        # self.btnExit.pack(side='bottom', padx=10, pady=5, anchor="sw")
        # self.btnReadWifiTx.config(state=tk.DISABLED)
        # self.btnReadWifiRx.config(state=tk.DISABLED)
        # self.btnReadWifiBeam.config(state=tk.DISABLED)
        # self.btnReadTxCalf33.config(state=tk.DISABLED)
        # self.btnReadTxCalf6.config(state=tk.DISABLED)
        # self.btnReadRxCalf32.config(state=tk.DISABLED)
        # self.btnReadRxCalf5.config(state=tk.DISABLED)
        #
        self.txt = tk.Text(self.frameTxt, font=self.font, width=200, height=150, wrap=tk.WORD)
        self.txt.pack(side='left')
        self.txt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
        # self.path = os.path.dirname(os.path.abspath('__file__'))
        # self.create_dataDir()
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        self.info_manager = InfoManager(self.txt)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def chooseFile(self):
        filePath = filedialog.askopenfilename()
        self.info_manager.update_info(f'Loading from file path', filePath)
        if filePath:
            try:
                with open(filePath, 'r') as file:
                    content = file.read()
                    df = utils.convertToDf(content)
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

    def ReadRawData(self, *args):
        table_mapping = {
            "Rx": {"func": utils.makeRxTable, "message": "WifiRx"},
            "Tx": {"func": utils.makeTxTable, "message": "WifiTx"},
            "BeamForm": {"func": utils.makeBeamFormTable, "message": "Wifi_BeamForm"},
            "TxCalf33": {"func": utils.makeWifiTxCalib33, "message": "Wifi Tx Calib33"},
            "TxCalf6": {"func": utils.makeWifiTxCalib6, "message": "Wifi Tx Calib6"},
            "RxCalf32": {"func": utils.makeWifiRxCalib32, "message": "Wifi Tx RxCalf32"},
            "RxCalf5": {"func": utils.makeWifiRxCalib5, "message": "Wifi Tx RxCalf5"}
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
        self.root.mainloop()

    def on_exit(self):  # obj: object
        # loop through all windows and destroy them
        for window in self.windows:
            window.destroy()
        self.root.destroy()

    # def DestroyDirectory(path: str):
    #     files = glob.glob(f'{path}/*')
    #     for f in files:
    #         os.remove(f)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.root = tk.Tk()
        self.windows = []
        self.root.geometry("750x600")
        self.root.title("Entrance")
        self.font = ('Times New Roman', 12, "bold")
        self.frame = tk.Frame(self.root, bg='gray66', width=100, height=160)
        # self.frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        self.frame.pack(side='left', fill=tk.BOTH, expand=False)
        self.frameTxt = tk.Frame(self.root, bg='gray78', width=100, height=160)
        self.frameTxt.pack(side='right', fill=tk.BOTH, expand=False)

        self.label = tk.Label(self.frame, font=('Times', 20, 'bold'), text="Load txt before output file!",
                              justify='left')
        self.label.pack(side='top', padx=5, pady=5)
        self.label.pack(side='top', padx=5, pady=5)
        self.btnOpen = tk.Button(self.frame, text="Open Txt", command=lambda: self.chooseFile())
        self.btnOpen.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnReadWifiTx = tk.Button(self.frame, text="Yield WIFI_TX_table", command=lambda: self.ReadRawData("Tx"))
        self.btnReadWifiTx.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnReadWifiRx = tk.Button(self.frame, text="Yield WIFI_RX_table", command=lambda: self.ReadRawData("Rx"))
        self.btnReadWifiRx.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnReadWifiBeam = tk.Button(self.frame, text="Yield WIFI_Beam_table",
                                         command=lambda: self.ReadRawData("BeamForm"))
        self.btnReadWifiBeam.pack(side='top', padx=10, pady=5, anchor="w")
        # self.btnClean = tk.Button(self.frame, text="Clean Data", command=lambda: self.ReadRawData(""))
        # self.btnClean.pack(side='top', padx=10, pady=5)
        self.btnReadTxCalf33 = tk.Button(self.frame, text="Yield Tx Calibration 33",
                                         command=lambda: self.ReadRawData("TxCalf33"))
        self.btnReadTxCalf33.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnReadTxCalf6 = tk.Button(self.frame, text="Yield Tx Calibration 6",
                                        command=lambda: self.ReadRawData("TxCalf6"))
        self.btnReadTxCalf6.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnReadRxCalf32 = tk.Button(self.frame, text="Yield Rx Calibration 32",
                                         command=lambda: self.ReadRawData("RxCalf32"))
        self.btnReadRxCalf32.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnReadRxCalf5 = tk.Button(self.frame, text="Yield Rx Calibration 5",
                                        command=lambda: self.ReadRawData("RxCalf5"))
        self.btnReadRxCalf5.pack(side='top', padx=10, pady=5, anchor="w")
        self.btnExit = tk.Button(self.frame, text="Close Window", command=lambda: self.root.quit())
        self.btnExit.pack(side='bottom', padx=10, pady=5, anchor="sw")
        self.btnReadWifiTx.config(state=tk.DISABLED)
        self.btnReadWifiRx.config(state=tk.DISABLED)
        self.btnReadWifiBeam.config(state=tk.DISABLED)
        self.btnReadTxCalf33.config(state=tk.DISABLED)
        self.btnReadTxCalf6.config(state=tk.DISABLED)
        self.btnReadRxCalf32.config(state=tk.DISABLED)
        self.btnReadRxCalf5.config(state=tk.DISABLED)

        self.txt = tk.Text(self.frameTxt, font=self.font, width=200, height=150, wrap=tk.WORD)
        self.txt.pack(side='left')
        self.txt.config(state=tk.DISABLED, spacing1=10, spacing2=5, padx=10, pady=10)
        self.path = os.path.dirname(os.path.abspath('__file__'))
        self.create_dataDir()
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # self.frames = {}
        # 
        # for F in (StartPage, PageOne, PageTwo):
        #     frame = F(container, self)
        #     self.frames[F] = frame
        #     frame.grid(row=0, column=0, sticky="nsew")
        #
        # self.show_frame(StartPage)
        # self.info_manager = InfoManager(self.txt)



        label = tk.Label(self, text="This is the Start Page")
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame(PageOne))
        button1.pack()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def chooseFile(self):
        filePath = filedialog.askopenfilename()
        self.info_manager.update_info(f'Loading from file path', filePath)
        if filePath:
            try:
                with open(filePath, 'r') as file:
                    content = file.read()
                    df = utils.convertToDf(content)
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
            "Rx": {"func": utils.makeRxTable, "message": "WifiRx"},
            "Tx": {"func": utils.makeTxTable, "message": "WifiTx"},
            "BeamForm": {"func": utils.makeBeamFormTable, "message": "Wifi_BeamForm"},
            "TxCalf33": {"func": utils.makeWifiTxCalib33, "message": "Wifi Tx Calib33"},
            "TxCalf6": {"func": utils.makeWifiTxCalib6, "message": "Wifi Tx Calib6"},
            "RxCalf32": {"func": utils.makeWifiRxCalib32, "message": "Wifi Tx RxCalf32"},
            "RxCalf5": {"func": utils.makeWifiRxCalib5, "message": "Wifi Tx RxCalf5"}
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
        self.root.mainloop()

    def on_exit(self):  # obj: object
        # loop through all windows and destroy them
        for window in self.windows:
            window.destroy()
        self.root.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is Page One")
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is Page Two")
        label.pack(side="top", fill="x", pady=10)
        button1 = tk.Button(self, text="Go to Start Page",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        button2 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    A_op = [[1, 2, 3] for _ in range(10)]
    B_op = [[4, 5, 6] for _ in range(10)]
    C_op = [[7, 8, 9] for _ in range(10)]
    DUT_1 = [A_op, B_op, C_op]
    USL = 5
    LSL = -5
    range_spec = USL - LSL
    # grr_instance = Gage(DUT_1, LSL, USL)
    # grr_instance.fmt_println()
    # grr_instance.rawData_handling(range_spec, DUT_1)
    app = GUIApp()
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
