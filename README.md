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
 Host IP  
 Should be set to `localhost`  
#### DB_DATABASE  
 Database name which should match username  
 Should be set to `computer-stats`  
#### DB_PORT  
 MySQL port  
 Should match your MySQL port (can be found in MAMP preferences-->ports)


I have not setup proper configuration for the android app yet so currently you must go in and edit two lines of code to have the proper IP and port. Inside MainActivity.java on line 38 and ViewStats.java on line 86 a url is set like so  
`url_computer_stats = new URI("http", "192.168.1.91:8888", "/computer-stats-connector/get_computer_stats.php", null, null);`  
you must change the IP `192.168.1.91:8888` to match the IP of the computer running your server and the port that Apache is using. (Apache port can be found in MAMP preferences-->ports)

Once you've edited the config files and .java files to properly interact with your server you need to run database-setup.py using the following command inside `/computer-stats-python-app` folder  
`python database-setup.py`  
You should get a success message.  
Note that this should only be run the first time you setup the program and that running this file again will clear all entries in your database.

You can now run the actual python app using the following command inside `/computer-stats-python-app` folder  
`python computer-stats.py`
This should open up a GUI for you to interact with the app with

Finally you can open android studio and select open an existing Android Studio project and select the `/computer-stats-android-app` folder. You can then build the program to your android device

Once you've succesfully built to your android device if you create a user in the python app and turn on the tracker and then use the user info to log into the android app you should be able to view your computers statistics.

## Notes
The instillation and running sections describe setting up the application for local use on a local server meaning your android device has to be connected to the same LAN as the computer you're monitoring (on the same Wi-Fi network). This could be circumvented by opening up the port for the Apache server so that the android app could connect from outside the network.

In the running section I tell you to edit two lines of code in order to allow the android app to function. This is obviously not ideal and the next thing I want to do is move those variables into the settings for the app so that you can just change the IP inside the application. This has the added benefit that you wouldn't need to compile the program yourself as I could just have a precompiled .apk file in the repository.

Inside the repo is a file named Program Outline which has a brief outline of what stats are currently tracked, what table they're stored in and stats that I plan on tracking in the future. Along with adding the other stats to the tracker I would also like to make the python application eventually also show the statistics that it is tracking to add some functionality for it running by itself.

When designing my application I considered using a direct connection between the python app and the android app instead of posting all the data to a table and then pulling from said table. I chose to go with the database as it would mean that I could more easily track stats over long periods of time since the table wouldn't be changed or lost in between sessions. If you where to scale this application up to a large user base using a database may not be feasible as the amount of fetch and update calls every second may be to stressful on the server.

To be able to scale up the application you would also need to rewrite the python side of the code as currently it directly edits the MySQL database. This means that if you hosted the database on a webserver anyone you distributed the application to would need to know your servers password in order to connect which makes it unsafe if you don't know who is going to be using the application. In order to fix this you would need to restructure the python app to be more like the android side and use calls to something like php scripts instead to read and write data to the table.