import tkinter as tk
import psutil
import time
import threading
import mysql.connector

mydb = mysql.connector.connect(host="localhost", port="8889", user="computer-stats", password="ouaGS1zjUeu5sW3x", database="computer-stats")
mycursor = mydb.cursor(buffered=True)

cpu_tracker_switch = True
master_switch = True

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.start_cpu_tracker_button = tk.Button(self)
        self.start_cpu_tracker_button["text"] = "Start tracking \nCPU usage"
        self.start_cpu_tracker_button["command"] = self.start_cpu_tracker
        self.start_cpu_tracker_button.grid(row=0,column=0)
        
        self.stop_cpu_tracker_button = tk.Button(self)
        self.stop_cpu_tracker_button["text"] = "Stop tracking \nCPU usage"
        self.stop_cpu_tracker_button["command"] = self.stop_cpu_tracker
        self.stop_cpu_tracker_button.grid(row=0,column=1)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.kill)
        self.quit.grid(row=1,columnspan=2)

    def cpu_tracker(self):
        def run ():
            while(cpu_tracker_switch==True):
                mydb.commit()
                sql = "SELECT cpu_percent FROM computer_id WHERE id = 5"
                mycursor.execute(sql)
                val = mycursor.fetchone()[0]
                print(val)
                time.sleep(1)
                if cpu_tracker_switch == False:
                    break
                if master_switch == False:
                    break
        thread = threading.Thread(target=run)
        thread.start()

    def start_cpu_tracker(self):
        global cpu_tracker_switch
        cpu_tracker_switch = True
        print('CPU Tracker On')
        self.cpu_tracker()

    def stop_cpu_tracker(self):
        global cpu_tracker_switch
        cpu_tracker_switch = False
        print('CPU Tracker Off')

    def kill(self):
        global master_switch
        master_switch = False
        root.destroy()


root = tk.Tk()
app = Application(master=root)
app.mainloop()