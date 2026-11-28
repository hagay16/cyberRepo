"""from scapy.all import *


SERVER_IP = get_if_addr(conf.iface)
PORT = 2026


def UDPFilter(p):
    return IP in p and UDP in p and p[IP].dst == SERVER_IP and p[UDP].sport == PORT and 32 <= p[UDP].dport <= 126

def UDPPrint(p):
    print(chr(p[UDP].dport), end="")

sniff(lfilter=UDPFilter, prn=UDPPrint, store=False)"""


from scapy.all import *

conf.verb = 0
conf.logLevel = logging.ERROR

SERVER_IP = get_if_addr(conf.iface)
PORT = 2026

expected_sequence = PORT
last_letter = None


def UDPFilter(p):
    return IP in p and UDP in p and \
        p[IP].dst == SERVER_IP and \
        p[UDP].sport >= PORT and \
        (32 <= p[UDP].dport <= 126)


def SendACK(p):
    ack = IP(src=SERVER_IP, dst=p[IP].src)/UDP(sport=p[UDP].dport,dport=p[UDP].sport)

    send(ack, verbose=False)


def UDPPrint(p):
    global expected_sequence, last_letter

    sequence = p[UDP].sport
    letter = p[UDP].dport

    if sequence == expected_sequence:
        print(chr(letter), end="")
        expected_sequence += 1
        last_letter = letter
        SendACK(p)

    elif sequence == expected_sequence - 1 and letter == last_letter:
        SendACK(p)


sniff(iface=[conf.iface, "lo"],lfilter=UDPFilter, prn=UDPPrint, store=False)

