import socket
import pickle

UDP_IP = "127.0.0.1"
UDP_PORT = int(input("Enter port number: "))


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    location = pickle.loads(data)

    for key in location:
        print(f"{key}: {location[key]}", end = "\t")

    print()

