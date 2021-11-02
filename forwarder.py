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
    """
    Takes in stdin until it finds an APRS packet to parse
    """
    while True:
        line = input()

        if re.match("^(?P<call>.+)>(?P<dest>.+),", line):
            line = line.split(" ")
            packet = line[1]
            break

        else:
            continue

    return packet


def packet_formatter(packet):
    """
    Reformat packet so aprslib works better
    """
    if ",:=" in packet:
        packet = packet.replace(",:=", ":!")

    return packet


def sender(parsed):
    """
    Send the latitude, longitude and altitude from the parsed packet
    """
    latitude = parsed["latitude"]
    longitude = parsed["longitude"]
    # altitude = parsed["altitude"]

    location = struct.pack("ff", latitude, longitude)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(location, (IP, PORT))


def main():
    """
    Main function
    """

    while True:
        APRS_packet = output_reader() # Loop until it finds an APRS packet 
        APRS_packet = packet_formatter(APRS_packet) # Hacky reformatting so packet works with aprslib

        try:
            parsed_packet = aprslib.parse(APRS_packet)

        except ParseError:
            print("Parse Error")
            continue

        sender(parsed_packet)


if __name__ == "__main__":
    main()
