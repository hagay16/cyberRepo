from scapy.all import *


SERVER_IP = get_if_addr(conf.iface)
PORT = 2026

def UDPFilter(p):
    return IP in p and UDP in p and Raw in p and p[IP].dst == SERVER_IP and p[UDP].dport == PORT

def UDPPrint(p):
    print(p[Raw].load.decode())

def StopFilter(p):
    return p[Raw].load == b"exit!"

sniff(lfilter=UDPFilter, prn=UDPPrint,stop_filter=StopFilter, store=False)