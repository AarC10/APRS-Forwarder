"""
Read and parse APRS packets
Author: Aaron Chan The Avionics Prodigy
"""

import re
import struct
import aprslib
import socket
import time
import sys

IP = "127.0.0.1"
PORT = 8081

def output_reader():
    while True:
        line = input()

        if re.match("^(?P<call>.+)>(?P<dest>.+),", line):
            line = line.split(" ")
            packet = line[1]
            break

        else:
            print("Invalid")
            continue

    return packet
    
def sender(parsed):
    latitude = parsed["latitude"]
    longitude = parsed["longitude"]

    lat_long = struct.pack("ff", latitude, longitude)
    
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.sendto(lat_long, (IP, PORT))


def main():
    packet = r"KD2WSM-5>APDR16,:=4307.61N07741.17WS433.290MHz" 
    parsed = aprslib.parse("KD2WSM-5>APDR16:!4307.61N\\07741.17WS433.290MHz")

    while True:
        APRS_packet = output_reader()
        print(APRS_packet)
        parsed_packet = aprslib.parse(APRS_packet)
        sender(parsed_packet)
        print("Sent")
        time.sleep(5)
    
    

if __name__ == "__main__":
    main()
