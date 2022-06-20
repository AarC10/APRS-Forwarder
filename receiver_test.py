import socket
import pickle
import struct

import pandas as pd

UDP_IP = input("Enter IP: ")
UDP_PORT = int(input("Enter port number: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

df = pd.DataFrame()

try:
	while True:
		data, addr = sock.recvfrom(1024)
		# location = pickle.loads(data)
		location = struct.unpack(">3f", data)

		print("Received:")
		# for key in location:
		# 	print(f"\t{key}: {location[key]}")
		print(data)
		print(location)

		print()
	# df = df.append(location, ignore_index=True)

except KeyboardInterrupt:
	print("\nExiting...")

	# df.to_excel("data/receiver_test.xlsx")

	sock.close()
