"""
Read and parse APRS packets
Author: Aaron Chan The Avionics Prodigy
"""

import re
import aprslib
import socket
import time
import sys
import pickle

from aprslib.exceptions import ParseError

try:
	args = sys.argv

	IP_AND_PORT = args[1].split(':')
	IP = IP_AND_PORT[0]
	PORT = int(IP_AND_PORT[1])
	CALLSIGN = args[2]

except IndexError:
	print("Usage: forwarder.py IP:PORT CALLSIGN")
	sys.exit(1)


def output_reader():
	"""
	Takes in stdin until it finds an APRS packet to parse
	"""
	while True:
		line = input()

		if re.match("^(?P<call>.+)>(?P<dest>.+)", line):
			line = line.split(" ")
			packet = line[1]
			break

		else:
			continue

	return packet

def sender(parsed):
	"""
	Send the latitude, longitude and altitude from the parsed packet
	"""
	location = dict()

	for key in parsed:
		if key == "latitude" or key == "longitude" or key == "altitude":
			location[key] = parsed[key]

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.sendto(pickle.dumps(location), (IP, PORT))


def main():
	"""
	Main function
	"""
	print("Forwarding to {}:{}".format(IP, PORT))
	print("Callsign: {}".format(CALLSIGN))

	while True:
		APRS_packet = output_reader()  # Loop until it finds an APRS packet

		parsed_packet = aprslib.parse(APRS_packet)

		if parsed_packet["from"] == CALLSIGN:
			sender(parsed_packet)


if __name__ == "__main__":
	main()
