import serial
import struct
import pandas as pd
from datetime import datetime

class Indicators:
	temperature: float
	humidity: float
	radoncur: float
	radonmax: float


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

def write():
    df=pd.DataFrame(columns=('datetime', 'temp', 'hum', 'radcur', 'radmax'))
    print(df)
    bit_string = b"\x7b\xff\x20\x00\x06\x00\x83\x04\x00\x00\xda\xfb\x04\x08\x0c\x00\xef\xf7"
    time1 = datetime.now()
    dt1 = time1
    time2 = datetime.now()
    dt2 = time2
    print(time2)
    while dt1.minute != 60:
        while dt1.minute == dt2.minute:
            time2 = datetime.now()
            dt2 = time2
        time1 = time2
        dt1 = time1
        ser.write(bit_string)
        raw_temp = b""
        raw_hum = b""
        raw_rad2 = b""
        raw_rad3 = b""
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
        new_row = pd.DataFrame({'datetime':time1, 'temp':temperature, 'hum':humidity, 'radcur':radoncur, 'radmax':radonmax}, index=[0])
        df = pd.concat([df,new_row],ignore_index=True)
        print(df)
    return(df)

time1 = datetime.now()
dt1 = time1
filename1 = 'a'+ '.csv'
time2 = datetime.now()
dt2 = time2
filename2 = str(dt2.hour) + '.csv'
while True:
    while filename1 == filename2:
        time2 = datetime.now()
        dt2 = time2
        filename2 = str(dt2.hour) + '.csv'
    time1 = time2
    dt1 = time1
    result_file = open(filename2, 'w')
    df = write()
    df.to_csv(result_file, index=False)

