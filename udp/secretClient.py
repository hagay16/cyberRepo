from scapy.all import *

while True:
    message = input("Enter secret message or exit: ")

    chars = list(message)
    for c in chars:
        port = ord(c)
        #print(f"{port} ")
        print(f"{c}", end="")