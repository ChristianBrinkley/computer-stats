# computer-stats

## About
computer-stats tracks computer statistics and adds them to a MySQL database to later be pulled by an android app that displays these statistics on your android device.   
computer-stats contains three parts: 
- A python application which runs on your computer to track and updates a MySQL table with statistics such as cpu and memory usage.
- A android application which calls for statistics from the MySQL database containing computer statistics and displays them.
- A few PHP scripts which are called by the android application to fetch the data from the MySQL database.

## Prerequisites

### Required Software:
- [python 3.7](https://www.python.org/downloads/release/python-370/)
- [android studio](https://developer.android.com/studio/)
- local server ([MAMP](https://www.mamp.info/en/))

### Required Python Libraries:
- [psutil](https://psutil.readthedocs.io/en/latest/)
- [mysql.connector](https://dev.mysql.com/doc/connector-python/en/)
- [passlib](https://passlib.readthedocs.io/en/stable/)

## Installation
Installing and using computer-stats requires the user to be able to host your own local server with a MySQL database. For instructions on installing MAMP you can [click here](https://documentation.mamp.info/).
1. Clone repository `git clone https://github.com/ChristianBrinkley/computer-stats`
2. Inside the repository is a folder named `/computer-stats-connector` this folder needs to be moved into `/MAMP/htdocs`
3. To set up a new MySQL database create new user account with the following properties

   User name: computer-stats  
   Host name: localhost  
   Password can be whatever you want  
   Check the create database with same name and grant all privileges box  
   All other settings can be left as default  
   [Example](https://i.imgur.com/TCdkgT2.png)

## Running
Once you've setup your MySQL database you need to edit the config files which are located at `/computer-stats-connector/db_config.php` and `/computer-stats-python-app/db-config.ini`. The config variables are listed below.

### Config
#### DB_USERNAME  
 Username that is associated with database for this program  
 Should be set to `computer-stats`  
#### DB_PASSWORD  
 Password that is associated with Username  
 Should match what you entered when setting up MySQL database  
#### DB_HOST  
 Host ip  
 Should be set to `localhost`  
#### DB_DATABASE  
 Database name which should match username  
 Should be set to `computer-stats`  
#### DB_PORT  
 MySQL port  
 Should match your MySQL [port](https://i.imgur.com/xsgU9Al.png)

