#!/usr/bin/python

import os
import time
import MySQLdb

# mount the 1wire filesystem 
os.system("/usr/bin/owfs -C -uall -m /mnt/1wire --allow_other")

# turn on the appropriate 1wire branches
os.system("echo 1 > /mnt/1wire/EF.54A720150000/hub/branch.0")
os.system("echo 1 > /mnt/1wire/EF.54A720150000/hub/branch.1")

# get the database password out of the environment
db_password = os.environ['PASS_DB_HVAC']

# connect to the weather database
connection = MySQLdb.connect('weatherdb.aenea.org', 'house.user', db_password, 'weewx_archive')
cursor = connection.cursor()

# get the most recent outdoor temperature
query = "SELECT outTemp FROM weewx_archive.archive ORDER BY dateTime DESC LIMIT 1;"
cursor.execute(query)
row = cursor.fetchone()

tempExternal = row[0]

cursor.close()
connection.close()

# connect to the house monitor db
connection = MySQLdb.connect('weatherdb.aenea.org', 'house.user', db_password, 'house')
cursor = connection.cursor()

# read the supply and return temperatures from the 1wire temperature probes
tempSupply = float(open("/mnt/1wire/28.BC224A060000/temperature12", "r").read())
tempReturn = float(open("/mnt/1wire/28.2A514A060000/temperature12", "r").read())

tempSupply = (tempSupply * 1.8) + 32
tempReturn = (tempReturn * 1.8) + 32
timeStamp = time.strftime("%y-%m-%d %H:%M", time.gmtime())

# write the current data to the house monitor db
query = "INSERT INTO hvac(date,tempSupply,tempReturn,tempExternal) VALUES(%s,%s,%s,%s)"
args = (timeStamp, tempSupply, tempReturn, tempExternal)

cursor.execute(query, args)
connection.commit()

cursor.close()
connection.close()
