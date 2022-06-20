Dire Wolf version 1.4
Includes optional support for:  gpsd
ERROR - Could not open config file /home/will/direwolf.conf
Try using -c command line option for alternate location.
Audio device for both receive and transmit: default  (channel 0)
Channel 0: 1200 baud, AFSK 1200 & 2200 Hz, E+, 44100 sample rate.
Note: PTT not configured for channel 0. (Ignore this if using VOX.)
Ready to accept AGW client application 0 on port 8000 ...
Ready to accept KISS client application on port 8001 ...
Use -p command line option to enable KISS pseudo terminal.

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   ||||||_|_
[0.3] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   _||||____
[0.2] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   _||||____
[0.2] KD2WSM-5>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-3>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-2>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   _||||____
[0.2] KD2WSM-10>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-20>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

KD2WSM-5 audio level = 1(0/0)   [NONE]   |||||||__
[0.3] KD2WSM-50>APDR16,:=4307.61N\07741.17WS433.290MHz https://aprsdroid.org/

QRT"""
Read and parse APRS packets
Author: Aaron Chan The Avionics Prodigy
"""
from collections import defaultdict

import aprslib
import argparse
import pickle
import re
import socket
import struct
import time

from aprslib.exceptions import ParseError

def argument_parse():
	"""
	Argument parser returning IP and Callsigns:Ports
	"""
	parser = argparse.ArgumentParser(description='APRS Forwarder')

	single_or_multi = parser.add_mutually_exclusive_group()
	single_or_multi.add_argument('-s', '--single', nargs=2, help='Assign a single port to forward a single callsign to')
	single_or_multi.add_argument('-m', '--multi', nargs="*",
								 help='Assign multiple ports to forward multiple callsigns to')

	parsed_args = parser.parse_args()

	if parsed_args.single:
		ip_and_port = parsed_args.single[0]
		ip_and_port = ip_and_port.split(":")
		ip = ip_and_port[0]
		port = int(ip_and_port[1])
		callsign = parsed_args.single[1]

		print("Assigning {} to {}".format(port, callsign))

		return ip, {callsign: port}

	elif parsed_args.multi:
		ip = parsed_args.multi[0]

		if not re.match("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
			print("Invalid IP address. Please try again.")
			exit()

		callsign_port_pair = dict()

		for i in range(1, len(parsed_args.multi)):
			callsign, port = parsed_args.multi[i].split(":")
			callsign_port_pair[callsign] = int(port)

		print("Port Assignments:")
		for callsign in callsign_port_pair:
			print("\t{} -> {}".format(callsign, callsign_port_pair[callsign]))

		return ip, callsign_port_pair

def packet_formatter(packet):
	"""
	Reformat packet so aprslib works better
	"""
	if ",:=" in packet:
		packet = packet.replace(",", "")

	return packet

def output_reader():
	"""
	Takes in stdin until it finds an APRS packet to parse
	"""
	while True:
		try:
			line = input()

		except UnicodeDecodeError:
			print("Can't decode byte")

		if re.match("^(?P<call>.+)>(?P<dest>.+)", line):

				line = line.split(" ")
				packet = line[1]
				return packet

		else:
			continue

def sender(parsed):
	"""
	Send the latitude, longitude and altitude from the parsed packet
	"""
	location = defaultdict()
	location.setdefault(-1)

	for key in parsed:
		if key == "latitude" or key == "longitude" or key == "altitude":
			location[key] = parsed[key]

	packet = struct.pack('>3f',
		location.get("latitude", float('nan')),
		location.get("longitude", float('nan')),
		location.get("altitude", float('nan'))
	)

	print(location.get("latitude", -1.0),
		location.get("longitude", -1.0),
		location.get("altitude", -1.0))

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print(location)
	print(packet)
	sock.sendto(packet, (IP, CALLSIGN_PORT_PAIR[parsed["from"]]))

def main():
	"""
	Main function
	"""
	while True:
		APRS_packet = output_reader()  # Loop until it finds an APRS packet

		try:
			parsed_packet = aprslib.parse(APRS_packet)

		except ParseError:
			parsed_packet = aprslib.parse(packet_formatter(APRS_packet))

		if parsed_packet["from"] in CALLSIGN_PORT_PAIR:
			sender(parsed_packet)

if __name__ == "__main__":
	IP, CALLSIGN_PORT_PAIR = argument_parse()
	main()
