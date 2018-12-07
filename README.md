# computer-stats
computer-stats contains three parts: 
- A python application which runs on your computer to track and updates a mySQL table with statistics such as cpu and memory usage.
- A android application which calls for statistics from the mySQL database containing computer statistics and displays them.
- A few PHP scripts which are called by the android application to fetch the data from the mySQL database.

## Prerequisites
### Required Software:
- python 3.7
- android studio
- local server (such as MAMP)
### Required Python Libraries:
- [psutil](https://psutil.readthedocs.io/en/latest/)
- [mysql.connector](https://dev.mysql.com/doc/connector-python/en/)
- [passlib](https://passlib.readthedocs.io/en/stable/)

## Instilation
1. Configure files to properly connect to 
2. Setting up mySQL database
   - Create new user account with name computer-stats and a database with the same name and is granted all privliages. [Example](https://imgur.com/a/iHp8gSY)
   -
