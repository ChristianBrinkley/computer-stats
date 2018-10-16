import tkinter as tk
import psutil
import time
import threading
import mysql.connector
from passlib.hash import sha256_crypt
import uuid
import datetime

mydb = mysql.connector.connect(host="localhost", port="8889", user="computer-stats", password="ouaGS1zjUeu5sW3x", database="computer-stats")
mycursor = mydb.cursor(buffered=True)

master_switch = True

class User(object):

    computer_stats_tracker_switch = True
    track_cpu = True
    track_memory = True
    track_disk = True

    def __init__(self, cid, computer_name, password, disks):
        self.cid = cid
        self.computer_name = computer_name
        self.password = password
        self.disks = disks


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

        label1 = tk.Label(self, text="Please enter computer name and password", font=controller.title_font, wraplength=300, justify='center')
        label2 = tk.Label(self, text="Computer Name:", font=controller.reg_font)
        label3 = tk.Label(self, text="Password:", font=controller.reg_font)
        label4 = tk.Label(self, textvariable=self.error_message, font=self.controller.err_font, fg="red", wraplength=270, justify='left')

        entry1 = tk.Entry(self)
        entry2 = tk.Entry(self)

        button1 = tk.Button(self, text="LOGIN", command=lambda: self.login(computerName=entry1.get(), password=entry2.get()))
        button2 = tk.Button(self, text="QUIT", command=controller.kill)
        button3 = tk.Button(self, text="NEW USER", command=lambda: self.newUser(computerName=entry1.get(), password=entry2.get()))

        label1.grid(row=0, column=0, columnspan=3, sticky='w')
        label2.grid(row=1, column=0, sticky='e')
        label3.grid(row=2, column=0, sticky='e')
        label4.grid(row=3, column=0, columnspan=3, sticky='w')
        
        entry1.grid(row=1, column=1)
        entry2.grid(row=2, column=1)

        button1.grid(row=4, column=0, sticky='we')
        button3.grid(row=4, column=1, sticky='we')
        button2.grid(row=4, column=2, sticky='we')
    
    def login(self, computerName, password):
        sql = "SELECT password FROM user WHERE computer_name = %s"
        val = (computerName,)
        mycursor.execute(sql, val)
        row_count = mycursor.rowcount
        if((row_count != 0) and sha256_crypt.verify(str(password), mycursor.fetchone()[0])):
            sql = "SELECT * FROM user WHERE computer_name = %s"
            mycursor.execute(sql, val)
            val = mycursor.fetchone()
            self.controller.user = User(cid=val[1], computer_name=val[2], password=val[3], disks=psutil.disk_partitions())
            for disk in self.controller.user.disks:
                sql = "SELECT * FROM disks WHERE (cid=%s) AND (disk_path = %s)"
                val = (self.controller.user.cid, disk[0])
                mycursor.execute(sql, val)
                row_count = mycursor.rowcount
                if(row_count==0):
                    sql = "INSERT INTO disks (cid, disk_path) VALUES (%s, %s)"
                    val =(self.controller.user.cid, disk[0])
                    mycursor.execute(sql, val)
            mydb.commit()  
            self.controller.show_frame("MainPage")
        else:
            self.error_message.set('Computer name or password is incorrect.')      
    
    def newUser(self, computerName, password):
        sql = "SELECT * FROM user WHERE computer_name = %s"
        val = (computerName,)
        mycursor.execute(sql, val)
        row_count = mycursor.rowcount
        if(row_count <= 0 and len(computerName) > 3 and len(password) > 3):
            cid = uuid.uuid4()
            cid = str(cid)
            sql = "INSERT INTO user (cid, computer_name, password) VALUES (%s, %s, %s)"
            val = (cid, computerName, sha256_crypt.encrypt(password))
            mycursor.execute(sql, val)
            sql = "INSERT INTO stats (cid) VALUES (%s)"
            val = (cid,)
            mycursor.execute(sql, val)
            disks = psutil.disk_partitions()
            for disk in disks:
                sql = "INSERT INTO disks (cid, disk_path) VALUES (%s, %s)"
                val =(cid, disk[0])
                mycursor.execute(sql, val)
            mydb.commit()
            sql = "SELECT * FROM user WHERE computer_name = %s"
            val = (computerName,)
            mycursor.execute(sql, val)
            val = mycursor.fetchone()
            self.controller.user = User(cid=val[1], computer_name=val[2], password=val[3], disks=disks)
            self.controller.show_frame("MainPage")
        else:
            if(row_count > 0):
                self.error_message.set("Computer name already taken.")
            elif (len(computerName) <= 3 and len(password) <= 3):
                self.error_message.set("Computer name and password must be longer than 3 characters.")
            elif (len(computerName) <= 3):
                self.error_message.set("Computer name must be longer than 3 characters.")
            elif (len(password) <= 3):
                self.error_message.set("Password must be longer than 3 characters.")
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label_title = tk.Label(self, text="Welcome to ComputerStats", font=controller.title_font)

        button_quit = tk.Button(self, text="QUIT", command=controller.kill)
        button_start = tk.Button(self, text="Start Monitoring", command=self.start_tracker)
        button_stop = tk.Button(self, text="Stop Monitoring", command=self.stop_tracker)
        button_settings = tk.Button(self, text="SETTINGS", command=lambda: self.controller.show_frame("SettingsPage"))

        label_title.grid(row=0, column=0, columnspan=2)

        button_start.grid(row=1, column=0, sticky='we', padx=5, pady=5)
        button_stop.grid(row=1, column=1, sticky='we', padx=5, pady=5)
        button_quit.grid(row=2, column=0, sticky='we', padx=5, pady=5)
        button_settings.grid(row=2, column=1, sticky='we', padx=5, pady=5)

    def tracker(self):
        def run ():
            system_boot_time = psutil.boot_time()
            computer_user = psutil.users()[0][0]
            cpu_count_physical = psutil.cpu_count(logical=False)
            cpu_count_logical = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()[2]
            memory_total = round(psutil.virtual_memory()[0]/1073741824, 2)
            sql = "UPDATE stats SET system_boot_time = %s, computer_user = %s, cpu_count_physical = %s, cpu_count_logical = %s, cpu_frequency = %s, memory_total = %s WHERE cid = %s"
            val = (datetime.datetime.fromtimestamp(system_boot_time).strftime("%Y-%m-%d %H:%M:%S"), computer_user, cpu_count_physical, cpu_count_logical, cpu_freq, memory_total, self.controller.user.cid)
            mycursor.execute(sql, val)
            while(self.controller.user.computer_stats_tracker_switch == True):
                if(self.controller.user.track_cpu == True):
                    self.update_cpu()
                if(self.controller.user.track_memory == True):
                    self.update_memory()
                if(self.controller.user.track_disk == True):
                    self.update_disks()
                mydb.commit()
                time.sleep(1)
                if self.controller.user.computer_stats_tracker_switch == False:
                    break
                if master_switch == False:
                    break
            sql = "UPDATE user SET tracking_all_stats = DEFAULT WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
            sql = """UPDATE stats SET cpu_percent = DEFAULT, 
                cpu_max_percent = DEFAULT,
                cpu_count_physical = DEFAULT,
                cpu_count_logical = DEFAULT,
                cpu_frequency = DEFAULT,
                memory_total = DEFAULT,
                memory_available = DEFAULT,
                memory_used = DEFAULT,
                memory_percent = DEFAULT
                WHERE cid = %s"""
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
            sql = """UPDATE disks SET disk_total = DEFAULT,
                disk_used = DEFAULT,
                disk_free = DEFAULT,
                disk_percent = DEFAULT
                WHERE cid = %s"""
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)            
            mydb.commit()
        thread = threading.Thread(target=run)
        thread.start()
    
    def update_cpu(self):
        sql = "SELECT cpu_max_percent FROM stats WHERE cid = %s"
        val = (self.controller.user.cid,)
        mycursor.execute(sql,val)
        previous_max = mycursor.fetchone()
        current_cpu = psutil.cpu_percent()
        if(previous_max[0]<current_cpu):
            sql_u = "UPDATE stats SET cpu_percent = %s, cpu_max_percent = %s WHERE cid = %s"
            val_u = (current_cpu, current_cpu, self.controller.user.cid)
        else:
            sql_u = "UPDATE stats SET cpu_percent = %s WHERE cid = %s"
            val_u = (current_cpu, self.controller.user.cid)
        mycursor.execute(sql_u,val_u)

    def update_memory(self):
        memory = psutil.virtual_memory()
        sql = "UPDATE stats SET memory_available = %s, memory_used = %s, memory_percent = %s WHERE cid = %s"
        val = (round(memory[1]/1073741824, 2), round(memory[3]/1073741824, 2), memory[2], self.controller.user.cid)
        mycursor.execute(sql, val)

    def update_disks(self):
        old_disks = self.controller.user.disks
        self.controller.user.disks = psutil.disk_partitions()
        for old_disk in old_disks:
            exist = False
            for new_disk in self.controller.user.disks:
                if(new_disk[0]==old_disk[0]):
                    exist = True
            if(not exist):
                sql = "UPDATE disks SET disk_total = DEFAULT, disk_used = DEFAULT, disk_free = DEFAULT, disk_percent = DEFAULT WHERE (cid = %s) and (disk_path = %s)"
                val =(self.controller.user.cid, old_disk[0])
                mycursor.execute(sql, val)
        for disk in self.controller.user.disks:
            sql = "SELECT * FROM disks WHERE (cid=%s) AND (disk_path = %s)"
            val = (self.controller.user.cid, disk[0])
            mycursor.execute(sql, val)
            row_count = mycursor.rowcount
            if(row_count==0):
                try:
                    sql = "INSERT INTO disks (cid, disk_path, disk_total, disk_used, disk_free, disk_percent) VALUES (%s, %s, %s, %s, %s, %s)"
                    disk_stats = psutil.disk_usage(disk[0])
                    val = (self.controller.user.cid, disk[0], round(disk_stats[0]/1073741824, 2), round(disk_stats[1]/1073741824, 2), round(disk_stats[2]/1073741824, 2), disk_stats[3])
                    mycursor.execute(sql, val)
                except:
                    pass
            else:
                try:
                    sql = "UPDATE disks SET disk_total = %s, disk_used = %s, disk_free = %s, disk_percent = %s WHERE (cid = %s) and (disk_path = %s)"
                    disk_stats = psutil.disk_usage(disk[0])
                    val =(round(disk_stats[0]/1073741824, 2), round(disk_stats[1]/1073741824, 2), round(disk_stats[2]/1073741824, 2), disk_stats[3], self.controller.user.cid, disk[0])
                    mycursor.execute(sql, val)
                except:
                    sql = "UPDATE disks SET disk_total = DEFAULT, disk_used = DEFAULT, disk_free = DEFAULT, disk_percent = DEFAULT WHERE (cid = %s) and (disk_path = %s)"
                    val = (self.controller.user.cid, disk[0])
                    mycursor.execute(sql, val)        

    def start_tracker(self):
        self.controller.user.computer_stats_tracker_switch = True
        print('CPU Tracker On')
        sql = "UPDATE user SET tracking_all_stats = 1 WHERE cid = %s"
        val = (self.controller.user.cid,)
        mycursor.execute(sql, val)
        mydb.commit()
        self.tracker()

    def stop_tracker(self):
        self.controller.user.computer_stats_tracker_switch = False
        print('CPU Tracker Off')

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        cpuToggle = tk.IntVar(None, 1)
        memoryToggle = tk.IntVar(None, 1)
        diskToggle = tk.IntVar(None, 1)
        
        title_label = tk.Label(self, text="Settings", font=controller.title_font)
        cpu_toggle_label = tk.Label(self, text="CPU Usage:", font=controller.reg_font)
        memory_toggle_label = tk.Label(self, text="Memory Usage:", font=controller.reg_font)
        disk_toggle_label = tk.Label(self, text="Disk Usage:", font=controller.reg_font)

        cpu_on = tk.Radiobutton(self, text="ON", indicatoron = 1, variable = cpuToggle, value = 1)
        cpu_off = tk.Radiobutton(self, text="OFF", indicatoron = 1, variable = cpuToggle, value = 0)
        memory_on = tk.Radiobutton(self, text="ON", indicatoron = 1, variable = memoryToggle, value = 1)
        memory_off = tk.Radiobutton(self, text="OFF", indicatoron = 1, variable = memoryToggle, value = 0)
        disk_on = tk.Radiobutton(self, text="ON", indicatoron = 1, variable = diskToggle, value = 1)
        disk_off = tk.Radiobutton(self, text="OFF", indicatoron = 1, variable = diskToggle, value = 0)

        back_button = tk.Button(self, text="BACK", command=lambda: self.controller.show_frame("MainPage"))
        quit_button = tk.Button(self, text="QUIT", command=controller.kill)
        save_button = tk.Button(self, text="SAVE", command=lambda: self.update_settings(cpuToggle=cpuToggle.get(), memoryToggle = memoryToggle.get(), diskToggle = diskToggle.get()))

        title_label.grid(row=0, column=0)
        cpu_toggle_label.grid(row=1, column=0, sticky="e")
        memory_toggle_label.grid(row=2, column=0, sticky="e")
        disk_toggle_label.grid(row=3, column=0, sticky="e")

        cpu_on.grid(row=1, column=1)
        cpu_off.grid(row=1, column=2)
        memory_on.grid(row=2, column=1)
        memory_off.grid(row=2, column=2)
        disk_on.grid(row=3, column=1)
        disk_off.grid(row=3, column=2)

        back_button.grid(row=4, column=0)
        save_button.grid(row=4, column=1)
        quit_button.grid(row=4, column=2)

    def update_settings(self, cpuToggle, memoryToggle, diskToggle):
        if (cpuToggle == 1):
            self.controller.user.track_cpu = True
            sql = "UPDATE user SET tracking_cpu = DEFAULT WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
        elif(cpuToggle == 0):
            self.controller.user.track_cpu = False
            sql = "UPDATE user SET tracking_cpu = 0 WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
        if (memoryToggle == 1):
            self.controller.user.track_memory = True
            sql = "UPDATE user SET tracking_memory = DEFAULT WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
        elif(memoryToggle == 0):
            self.controller.user.track_memory = False
            sql = "UPDATE user SET tracking_memory = 0 WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
        if(diskToggle == 1):
            self.controller.user.track_disk = True
            sql = "UPDATE user SET tracking_disk = DEFAULT WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
        elif(diskToggle == 0):
            self.controller.user.track_disk = False
            sql = "UPDATE user SET tracking_disk = 0 WHERE cid = %s"
            val = (self.controller.user.cid,)
            mycursor.execute(sql, val)
        mydb.commit()

if __name__ == "__main__":
    app = ComputerStatsApp()
    app.protocol("WM_DELETE_WINDOW", app.kill)
    app.mainloop()