"""from scapy.all import *

conf.verb = 0
conf.logLevel = logging.ERROR

SERVER_IP = "10.0.0.18"
PORT = 2026

pack = IP(dst=SERVER_IP)/UDP(sport=PORT)

while True:
    msg = input("Enter a secret message: ")

    for letter in msg:
        pack[UDP].dport = ord(letter)
        send(pack, verbose=False)"""


from scapy.all import *


conf.verb = 0
conf.logLevel = logging.ERROR

SERVER_IP = "10.0.0.18"
CLIENT_IP = get_if_addr(conf.iface)
PORT = 2026
TIMEOUT = 5

sequence = PORT

pack = IP(src=CLIENT_IP, dst=SERVER_IP)/UDP(sport=PORT)

def ACKFilter(p):
    return IP in p and UDP in p and \
        p[IP].src == SERVER_IP and \
        p[IP].dst == CLIENT_IP and \
        p[UDP].sport == pack[UDP].dport and \
        p[UDP].dport == pack[UDP].sport


while True:
    msg = input("Enter a secret message: ")

    for letter in msg:
        pack[UDP].sport = sequence
        pack[UDP].dport = ord(letter)

        while True:
            response = sniff(iface=[conf.iface, "lo"],count=1,timeout=TIMEOUT,lfilter=ACKFilter,started_callback=lambda: send(pack, verbose=False))

            if len(response) > 0:
                sequence += 1
                break

            print("Timeout, resending packet...")