from scapy.all import *

conf.verb = 0
conf.logLevel = logging.ERROR

SERVER_IP = "10.0.0.18"
PORT = 2026


pack = IP(dst=SERVER_IP)/UDP(dport=PORT)/Raw()

while True:
    msg = input("Enter a 5-character word: ")

    if len(msg.encode()) != 5:
        print("Invalid message length")
        continue

    pack[Raw].load = msg.encode()
    send(pack, verbose=False)

    if msg == "exit!":
        break