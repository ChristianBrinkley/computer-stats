import configparser
import sys

config = configparser.ConfigParser()
config.read('db-config.ini')

try:
    import mysql.connector
except ImportError:
    sys.exit("Failed to import mysql.connector")

try:
    mydb = mysql.connector.connect(host=config['DEFAULT']['host'], port=config['DEFAULT']['port'], user=config['DEFAULT']['user'], password=config['DEFAULT']['password'], database=config['DEFAULT']['database'])
except:
    sys.exit("Failed to connect to mysql database")

mycursor = mydb.cursor()

sql = """DROP TABLE disks"""

try:
    mycursor.execute(sql)
except:
    pass

sql = """DROP TABLE stats"""

try:
    mycursor.execute(sql)
except:
    pass

sql = """DROP TABLE user"""

try:
    mycursor.execute(sql)
except:
    pass

sql = """CREATE TABLE user ( 
    id INT PRIMARY KEY AUTO_INCREMENT,
    cid VARCHAR(255) UNIQUE,
    computer_name VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    tracking_all_stats TINYINT DEFAULT 0,
    tracking_cpu TINYINT DEFAULT 1,
    tracking_memory TINYINT DEFAULT 1,
    tracking_disk TINYINT DEFAULT 1)"""

mycursor.execute(sql)

sql = """CREATE TABLE stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cid VARCHAR(255),
    cpu_percent DOUBLE DEFAULT 0,
    cpu_max_percent DOUBLE DEFAULT 0,
    cpu_count_physical INT DEFAULT 0,
    cpu_count_logical INT DEFAULT 0,
    cpu_frequency DOUBLE DEFAULT 0,
    memory_total DOUBLE DEFAULT 0,
    memory_available DOUBLE DEFAULT 0,
    memory_used DOUBLE DEFAULT 0,
    memory_percent DOUBLE DEFAULT 0,
    system_boot_time DATETIME,
    computer_user VARCHAR(255),
    FOREIGN KEY (cid) REFERENCES user(cid)
    )"""

mycursor.execute(sql)

sql = """CREATE TABLE disks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cid VARCHAR(255),
    disk_path VARCHAR(255),
    disk_total DOUBLE DEFAULT 0,
    disk_used DOUBLE DEFAULT 0,
    disk_free DOUBLE DEFAULT 0,
    disk_percent DOUBLE DEFAULT 0,
    FOREIGN KEY (cid) REFERENCES user(cid)
    )"""

mycursor.execute(sql)

mydb.commit()

print("Database succesfully setup.")
