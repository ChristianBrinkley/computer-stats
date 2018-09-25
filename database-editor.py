import mysql.connector

mydb = mysql.connector.connect(host="localhost", port="8889", user="computer-stats", password="ouaGS1zjUeu5sW3x", database="computer-stats")

mycursor = mydb.cursor()

mycursor.execute("""CREATE TABLE computer_id (
                    id INT AUTO_INCREMENT PRIMARY KEY, 
                    computer_name VARCHAR(128), 
                    password VARCHAR(128), 
                    cpu_percent DOUBLE, 
                    cpu_max_percent DOUBLE)""")
