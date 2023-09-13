import serial
import struct
import time
import pandas as pd
from datetime import datetime

class Indicators:
	temperature: float
	humidity: float
	radoncur: float
	radonmax: float

result_file = open('file.csv', 'w')

df=pd.DataFrame(columns=('datetime', 'temp', 'hum', 'radcur', 'radmax'))
print(df)
bit_string = "\x7b\xff\x20\x00\x06\x00\x83\x04\x00\x00\xda\xfb\x04\x08\x0c\x00\xef\xf7"

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

def get_indicators(bit_string):
	ser.write(bit_string)
	raw_temp = ""
	raw_hum = ""
	raw_rad2 = ""
	raw_rad3 = ""

	exp_timer = 0

	for x in range(0, 70):
		c = ser.read()
		#print('{0:x}'.format(ord(c), 10), " ")
		if x in range(28, 32):
			raw_rad3 = raw_rad3 + c
		if x in range(32, 36):
			raw_temp = raw_temp + c
		if x in range(36, 40):
			raw_hum = raw_hum + c
		if x in range(56, 60):
			raw_rad2 = raw_rad2 + c
		if x == 64:
			exp_timer = ord(c)
		if x == 65:
			exp_timer = ord(c) * 256 + exp_timer
	temperature = struct.unpack('f', raw_temp)
	humidity = struct.unpack('f', raw_hum)
	radoncur = struct.unpack('f', raw_rad3)
	radonmax = struct.unpack('f', raw_rad2)	
	return(temperature, humidity, radoncur, radonmax)


def make_df(temperature, humidity, radoncur, radonmax):
	now = datetime.now()
	new_row = pd.DataFrame({'datetime':now, 'temp':temperature, 'hum':humidity, 'radcur':radoncur, 'radmax':radonmax}, index=[0])
	df = pd.concat([new_row,df.loc[:]]).reset_index(drop=True)
	

ser.isOpen()
print(ser.name) 
print(ser.is_open)


make_df(get_indicators(bit_string))
df.to_csv(result_file, index=False)


