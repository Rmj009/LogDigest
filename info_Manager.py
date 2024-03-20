import threading
import time
from tkinter import scrolledtext


class InfoManager:
    def __init__(self, txt_widget):
        self.font = ('Times New Roman', 12, "bold")
        self.txt_widget = txt_widget
        self.info = {}

    def __truediv__(self, other):
        line = "=" * len(other.count)
        return "\n".join([self.txt_widget, line, other.count])

    def update_info(self, title, info):

        try:
            self.info[title] = info
            self.update_text_widget()

        # ConfigTxt = tk.Text(self.frame, font=self.font, width=80, height=60, bg='white', fg='black')
        # ConfigTxt.insert(tk.END, f'{configFile} \n')
        except Exception as e:
            raise "update_info NG >>> " + str(e.args)
        finally:
            self.info = {}
            print('-------------------------------')

    def get_info(self, title):
        return self.info.get(title, "")

    def run_info_manager(self):
        # txt_widget = scrolledtext.ScrolledText(self.txt_widget, font=('Times New Roman', 12), wrap=tk.WORD)
        # txt_widget.pack(expand=True, fill='both', side='left')
        try:
            while True:
                # self.update_info("Time", time.ctime())
                self.update_info("Processing", "...")
                time.sleep(0.01)
                break
        except Exception as e:
            raise "run_info_manager NG >>> " + str(e.args)

    def update_text_widget(self):
        self.txt_widget.config(state='normal')
        # self.txt_widget.delete(self.txt_widget, tk.END)
        for title, info in self.info.items():
            self.txt_widget.insert('end', f">>> {title} \n" + ">>> " + f"{info} \r\n")
            self.txt_widget.see('end')
        self.txt_widget.config(state='disabled')

    def start_info_manager_thread(self):
        global info_manager_thread
        info_manager_thread = threading.Thread(target=self.run_info_manager)
        info_manager_thread.daemon = True
        info_manager_thread.start()
