"""
Receives APRS data, timestamps them and gets duration since first packet
Designed for testing battery life on BigRedBees

@author Aaron Chan
"""
import struct
import socket
import os
from datetime import datetime
from time import sleep

UDP_IP = input("Enter IP: ")
UDP_PORT = int(input("Enter port number: "))
DATE_TIME = str(datetime.now()).split(" ")
DATA_FOLDER = "../data/LOG-" + DATE_TIME[0] + "-" + DATE_TIME[1]



def handle_response(original_time):
    current_time = datetime.now()
    result_string = "Received packet at " + current_time.strftime("%H:%M:%S") + ". Time since first packet was " + str(current_time - original_time)
    print(result_string)
    os.system("echo " + result_string + "\ >> " + DATA_FOLDER)

def main():
    os.system("touch " + DATA_FOLDER)
    print("Logging to " + DATA_FOLDER)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    data_file = DATA_FOLDER + "LOG-" + str(datetime.now())

    try:
        data, addr = sock.recvfrom(1024)
        location = struct.unpack(">3d", data)
        original_time = datetime.now()

        while True:
            data, addr = sock.recvfrom(1024)
            location = struct.unpack(">3d", data)

            handle_response(original_time)

    except KeyboardInterrupt:
        print("\nExiting...")


        sock.close()

if __name__ == "__main__":
    main()

