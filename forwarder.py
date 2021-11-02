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

from aprslib.exceptions import ParseError

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

def packet_formatter(packet):
    if ",:=" in packet:
        packet = packet.replace(",:=", ":!")

    return packet
    
def sender(parsed):
    latitude = parsed["latitude"]
    longitude = parsed["longitude"]

    lat_long = struct.pack("ff", latitude, longitude)
    
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.sendto(lat_long, (IP, PORT))


def main():

    while True:
        APRS_packet = output_reader()
        APRS_packet = packet_formatter(APRS_packet)
        print(APRS_packet)
    
        try:
            parsed_packet = aprslib.parse(APRS_packet)

        except ParseError:
            print("Parse Error")
            continue
        sender(parsed_packet)
        
    

if __name__ == "__main__":
    main()
