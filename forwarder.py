"""
Read and parse APRS packets
Author: Aaron Chan The Avionics Prodigy
"""

import re
import struct
import aprslib
import socket


IP = "127.0.0.1"
PORT = 8081


def sender(parsed):
    # raw = parsed["raw"]
    # callsign = parsed["from"]
    # receiver = parsed["to"]
    # latitude = parsed["latitude"]
    # longitude = parsed["longitude"]
    # message = parsed["comment"]
    # sender_to_receiver = "./aprs_fwd %s:%s %s " %(IP, PORT, callsign)

    latitude = parsed["latitude"]
    longitude = parsed["longitude"]

    lat_long = struct.pack("ff", latitude, longitude)
    
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.sendto(lat_long, (IP, PORT))



def main():
    packet = r"KD2WSM-5>APDR16,:=4307.61N07741.17WS433.290MHz" 
    parsed = aprslib.parse("KD2WSM-5>APDR16:!4307.61N\\07741.17WS433.290MHz")

    while True:
        sender(parsed)
        # time.sleep(5)
    
    

if __name__ == "__main__":
    main()
