# sbchdr
python script to load HDR data to mysql

Configure on SBC, in system-config object. Allows collection of statistics on system and functions, and sending of such in form of csv files to remote server.
The 3 files below, when applied on linux server, will read the data and insert into mysql database, and perform graphing of system data (cpu,memory,cps)

The python script linked below can be run manually or automatically via crontab, or auto via command line by passing parameter "auto": 
linux# hr.py auto 

Example crontab entry:
30 * * * * /home/tluck/HDR/hr.py auto 2>&1 
You must create a database called sbchrd
- you can use the mysqldump file (the mysql db file) to import the db after the db is created.
linux# mysql -u <username> -p<username_password> sbchdr < dumpfilename.sql 
You must change the line in main that references the hdr.cfg file to your correct path

Currently, it will graph system cpu, memory, cps (calls per second), run run manually
linux# hr.py 
via command line in GUI on linux
