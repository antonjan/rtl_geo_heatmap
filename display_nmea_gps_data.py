import pynmea2
import datetime
nmea_data = open("data/gps_data_%Y%m%d-%H%M%S.nmea", "rb")
for message_bytes in nmea_data.readlines()[:10]: # read first 10 messages from file
    try:
        message = message_bytes.decode("utf-8").replace("\n", "").replace("\r", "")
        parsed_message = pynmea2.parse(message)
    except:
        # skip invalid messages
        continue
        
    print(f"message: {message}")

    for field in parsed_message.fields:
        value = getattr(parsed_message, field[1])
        print(f"{field[0]:40} {field[1]:20} {value}")
    
    print("\n")
