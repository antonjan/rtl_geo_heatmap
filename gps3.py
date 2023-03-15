import serial
import pandas as pd
import geopandas as gpd

port = "/dev/ttyACM0"
def parseGPS(data):
    print ("raw:", data) #prints raw data raw: b'$GPRMC,190722.00,A,2617.12440,S,02804.24041,E,0.118,,140323,,,D*64\r\n'
    #print (">>>> ",data[0:6])
    if data[0:6] == b'$GPRMC':
        print ("got GPRMC")
        sdata = data.decode().split(",")
        if sdata[2] == 'V':
            print ("no satellite data available")
            return
        print ("---Parsing GPRMC---",)
        time = sdata[1][0:2] + ":" + sdata[1][2:4] + ":" + sdata[1][4:6]
        lat = decode(sdata[3]) #latitude
        dirLat = sdata[4]      #latitude direction N/S
        lon = decode(sdata[5]) #longitute
        dirLon = sdata[6]      #longitude direction E/W
        speed = sdata[7]       #Speed in knots
        trCourse = sdata[8]    #True course
        date = sdata[9][0:2] + "/" + sdata[9][2:4] + "/" + sdata[9][4:6]#date
        print ("time : %s, latitude : %s(%s), longitude : %s(%s), speed : %s, True Course : %s, Date : %s" %  (time,lat,dirLat,lon,dirLon,speed,trCourse,date))
def decode(coord):
    #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    x = coord.split(".")
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"
 
print ("Receiving GPS data")
ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
while True:
   data = ser.readline()
   #print (data)
   parseGPS(data)
