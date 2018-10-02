import tkinter as tk
import psutil
import time
import threading
import mysql.connector
from passlib.hash import sha256_crypt

mydb = mysql.connector.connect(host="localhost", port="8889", user="computer-stats", password="ouaGS1zjUeu5sW3x", database="computer-stats")
mycursor = mydb.cursor(buffered=True)

master_switch = True

class User(object):

    computer_stats_tracker_switch = True
    track_cpu = True

    def __init__(self, computer_id, computer_name, password):
        self.computer_id = computer_id
        self.computer_name = computer_name
        self.password = password


class ComputerStatsApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = ('Helvetica', 14, "bold", "italic")
        self.reg_font = ('Helvetica', 12)
        self.err_font = ('Helvetica', 11, "italic")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginPage, MainPage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def kill(self):
        global master_switch
        master_switch = False
        self.destroy()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.error_message = tk.StringVar()

        label1 = tk.Label(self, text="Please enter computer name\nand password", font=controller.title_font)
        label2 = tk.Label(self, text="Computer Name:", font=controller.reg_font)
        label3 = tk.Label(self, text="Password:", font=controller.reg_font)
        label4 = tk.Label(self, textvariable=self.error_message, font=self.controller.err_font, fg="red")

        entry1 = tk.Entry(self)
        entry2 = tk.Entry(self)

        button1 = tk.Button(self, text="LOGIN", command=lambda: self.login(computerName=entry1.get(), password=entry2.get()))
        button2 = tk.Button(self, text="QUIT", command=controller.kill)
        button3 = tk.Button(self, text="NEW USER", command=lambda: self.newUser(computerName=entry1.get(), password=entry2.get()))

        label1.grid(row=0, column=0, columnspan=3)
        label2.grid(row=1, column=0, sticky='e')
        label3.grid(row=2, column=0, sticky='e')
        label4.grid(row=3, column=0, columnspan=4)
        
        entry1.grid(row=1, column=1)
        entry2.grid(row=2, column=1)

        button1.grid(row=4, column=0, sticky='we')
        button3.grid(row=4, column=1, sticky='we')
        button2.grid(row=4, column=2, sticky='we')
    
    def login(self, computerName, password):
        sql = "SELECT password FROM computer_id WHERE computer_name = %s"
        val = (computerName,)
        mycursor.execute(sql, val)
        row_count = mycursor.rowcount
        if((row_count != 0) and sha256_crypt.verify(str(password), mycursor.fetchone()[0])):
            sql = "SELECT * FROM computer_id WHERE computer_name = %s"
            mycursor.execute(sql, val)
            val = mycursor.fetchone()
            self.controller.user = User(computer_id=val[0], computer_name=val[1], password=val[2])
            self.controller.show_frame("MainPage")
        else:
            self.error_message.set('Computer name or password is incorrect.')      
    
    def newUser(self, computerName, password):
        sql = "SELECT * FROM computer_id WHERE computer_name = %s"
        val = (computerName,)
        mycursor.execute(sql, val)
        row_count = mycursor.rowcount
        if(row_count <= 0 and len(computerName) > 3 and len(password) > 3):
            sql = "INSERT INTO computer_id (computer_name, password, cpu_percent, cpu_max_percent) VALUES (%s, %s, 0, 0)"
            val = (computerName, sha256_crypt.encrypt(password))
            mycursor.execute(sql, val)
            mydb.commit()
            sql = "SELECT * FROM computer_id WHERE computer_name = %s"
            val = (computerName,)
            mycursor.execute(sql, val)
            val = mycursor.fetchone()
            self.controller.user = User(computer_id=val[0], computer_name=val[1], password=val[2])
            self.controller.show_frame("MainPage")
        else:
            if(row_count > 0):
                self.error_message.set("Computer name already taken.")
            elif (len(computerName) <= 3 and len(password) <= 3):
                self.error_message.set("Computer name and password must be\nlonger than 3 characters.")
            elif (len(computerName) <= 3):
                self.error_message.set("Computer name must be longer than 3\ncharacters.")
            elif (len(password) <= 3):
                self.error_message.set("Password must be longer than 3\ncharacters.")
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label1 = tk.Label(self, text="Welcome to ComputerStats", font=controller.title_font)

        button1 = tk.Button(self, text="LOGOUT")
        button2 = tk.Button(self, text="QUIT", command=controller.kill)
        button3 = tk.Button(self, text="Start Monitoring", command=self.start_tracker)
        button4 = tk.Button(self, text="Stop Monitoring", command=self.stop_tracker)
        button5 = tk.Button(self, text="SETTINGS", command=lambda: self.controller.show_frame("SettingsPage"))

        label1.grid(row=0, column=0, columnspan=5)

        button3.grid(row=1, column=1)
        button4.grid(row=1, column=3)
        button1.grid(row=2, column=0)
        button2.grid(row=2, column=2)
        button5.grid(row=2, column=4)

    def tracker(self):
        def run ():
            while(self.controller.user.computer_stats_tracker_switch == True):
                if(self.controller.user.track_cpu == True):
                    sql = "SELECT cpu_max_percent FROM computer_id WHERE id = %s"
                    val = (self.controller.user.computer_id,)
                    mycursor.execute(sql,val)
                    previous_max = mycursor.fetchone()
                    current_cpu = psutil.cpu_percent()
                    if(previous_max[0]<current_cpu):
                        sql_u = "UPDATE computer_id SET cpu_percent = %s, cpu_max_percent = %s WHERE id = %s"
                        val_u = (current_cpu, current_cpu, self.controller.user.computer_id)
                    else:
                        sql_u = "UPDATE computer_id SET cpu_percent = %s WHERE id = %s"
                        val_u = (current_cpu, self.controller.user.computer_id)
                    mycursor.execute(sql_u,val_u)
                mydb.commit()
                time.sleep(1)
                if self.controller.user.computer_stats_tracker_switch == False:
                    break
                if master_switch == False:
                    break
            sql = "UPDATE computer_id SET cpu_percent = %s, cpu_max_percent = %s WHERE id = %s"
            val = ('0', '0', self.controller.user.computer_id)
            mycursor.execute(sql,val)
            mydb.commit()
        thread = threading.Thread(target=run)
        thread.start()

    def start_tracker(self):
        self.controller.user.computer_stats_tracker_switch = True
        print('CPU Tracker On')
        self.tracker()

    def stop_tracker(self):
        self.controller.user.computer_stats_tracker_switch = False
        print('CPU Tracker Off')

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        cpuToggle = tk.IntVar(None, 1)
        
        label1 = tk.Label(self, text="Settings", font=controller.title_font)
        label2 = tk.Label(self, text="CPU Usage:", font=controller.reg_font)

        radio1 = tk.Radiobutton(self, text="ON", indicatoron = 1, variable = cpuToggle, value = 1)
        radio2 = tk.Radiobutton(self, text="OFF", indicatoron = 1, variable = cpuToggle, value = 0)

        button1 = tk.Button(self, text="BACK", command=lambda: self.controller.show_frame("MainPage"))
        button2 = tk.Button(self, text="QUIT", command=controller.kill)
        button3 = tk.Button(self, text="SAVE", command=lambda: self.update_settings(cpu=cpuToggle.get()))

        label1.grid(row=0, column=0)
        label2.grid(row=1, column=0, sticky="e")

        radio1.grid(row=1, column=1)
        radio2.grid(row=1, column=2)

        button1.grid(row=3, column=0)
        button3.grid(row=3, column=1)
        button2.grid(row=3, column=2)

    def update_settings(self, cpu):
        if (cpu == 1):
            self.controller.user.track_cpu = True
        elif(cpu == 0):
            self.controller.user.track_cpu = False

if __name__ == "__main__":
    app = ComputerStatsApp()
    app.mainloop()