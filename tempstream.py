import sqlite3 as lite
import os
import glob
import datetime
from ISStreamer.Streamer import Streamer

streamer = Streamer(bucket_name="Temperature Stream", bucket_key="OfficeTemp", access_key="fywFkJ2l8gP2yrxuIjtOfx6K08kkxGb3")

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def db_write(i, temp_f):
  con = lite.connect('/home/pi/dev/measure_db')
  cur = con.cursor()
  cur.execute('INSERT INTO temperatures VALUES(?, ?)', (i.isoformat() , temp_f) )
  con.commit()

def read_temp_raw():
     f = open(device_file, 'r')
     lines = f.readlines()
     f.close()
     return lines

def read_temp():
     lines = read_temp_raw()
     while lines[0].strip()[-3:] != 'YES':
          time.sleep(0.2)
          lines = read_temp_raw()
     equals_pos = lines[1].find('t=')
     if equals_pos != -1:
          temp_string = lines[1][equals_pos+2:]
          temp_c = float(temp_string) / 1000.0
          temp_f = temp_c * 9.0 / 5.0 + 32.0
          return temp_f

# while True:
temp_f = read_temp()
streamer.log("Temperature(F)", temp_f)
#     time.sleep(.5)
i = datetime.datetime.now()
db_write(i, temp_f)
