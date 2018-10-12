import mysql.connector

mydb = mysql.connector.connect(host="localhost", port="8889", user="computer-stats", password="ouaGS1zjUeu5sW3x", database="computer-stats")

mycursor = mydb.cursor()

#sql = """DROP TABLE 'storage-stats'"""

#mycursor.execute(sql)

sql = """DROP TABLE stats"""

mycursor.execute(sql)

sql = """DROP TABLE user"""

mycursor.execute(sql)

sql = """CREATE TABLE user ( 
    id INT PRIMARY KEY AUTO_INCREMENT,
    cid VARCHAR(255) UNIQUE,
    computer_name VARCHAR(255) UNIQUE,
    password VARCHAR(255))"""

mycursor.execute(sql)

sql = """CREATE TABLE stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cid VARCHAR(255),
    cpu_percent DOUBLE,
    cpu_max_percent DOUBLE,
    cpu_count INT,
    cpu_frequency DOUBLE,
    cpu_max_frequency DOUBLE,
    cpu_min_frequency DOUBLE,
    memory_total DOUBLE,
    memory_available DOUBLE,
    memory_used DOUBLE,
    memory_percent DOUBLE,
    system_boot_time DATETIME,
    computer_user VARCHAR(255),
    FOREIGN KEY (cid) REFERENCES user(cid)
    )"""

mycursor.execute(sql)

sql = """CREATE TABLE disks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cid VARCHAR(255),
    disk_path VARCHAR(255),
    disk_total DOUBLE,
    disk_used DOUBLE,
    disk_free DOUBLE,
    disk_percent DOUBLE,
    FOREIGN KEY (cid) REFERENCES user(cid)
    )"""

mycursor.execute(sql)

mydb.commit()
