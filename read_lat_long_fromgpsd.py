import gps

gpsd = gps.gps()
gpsd.stream(gps.WATCH_ENABLE|gps.WATCH_NEWSTYLE)

for report in gpsd:
    if report['class'] == 'TPV':
        print (report['lat'])
        print (report['lon'])
        break
