import socket
import pickle
import pandas as pd

UDP_IP = "127.0.0.1"
UDP_PORT = int(input("Enter port number: "))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

df = pd.DataFrame()

try:
	while True:
		data, addr = sock.recvfrom(1024)
		location = pickle.loads(data)

		print("Received:")
		for key in location:
			print(f"\t{key}: {location[key]}")

		print()
		df = df.append(location, ignore_index=True)

except KeyboardInterrupt:
	print("\nExiting...")

	try:
		df.to_excel("data/receiver_test.xlsx")
	except pd.xlsxwriter.exceptions.FileCreateError:
		pass

	sock.close()
