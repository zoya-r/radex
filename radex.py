import serial
import struct
import csv
from datetime import datetime


ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
print(ser.name) 
print(ser.is_open)

raw_temp = ""
raw_hum = ""
raw_rad2 = ""
raw_rad3 = ""


ser.write("\x7b\xff\x20\x00\x06\x00\x83\x04\x00\x00\xda\xfb\x04\x08\x0c\x00\xef\xf7")

exp_timer = 0;

for x in range(0, 70):
	c = ser.read()
	print('{0:x}'.format(ord(c), 10), " ")

	if x in range(28, 32):
		raw_rad3 = raw_rad3 + c
	if x in range(32, 36):
		raw_temp = raw_temp + c
	if x in range(36, 40):
		raw_hum = raw_hum + c
	if x in range(56, 60):
		raw_rad2 = raw_rad2 + c
	if x == 64:
		exp_timer = ord(c);
	if x == 65:
		exp_timer = ord(c) * 256 + exp_timer;

		
print("")
[temperature] = struct.unpack('f', raw_temp)
print("Temperature: " + str(temperature))
[humidity] = struct.unpack('f', raw_hum)
print("Humidity: " + str(humidity))
[radoncur] = struct.unpack('f', raw_rad3)
print("Radon Cur: " + str(radoncur))
[radonmax] = struct.unpack('f', raw_rad2)
print("Radon Max: " + str(radonmax))
print("Exposure countdown: " + str(exp_timer))
		
	