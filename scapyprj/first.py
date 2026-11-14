from scapy.all import *

conf.iface = r"\Device\NPF_Loopback"


def HTTPFilter(p):
    return TCP in p and Raw in p and p[Raw].load.startswith(b'GET')

def HTTPrint(p):
    print(p[Raw].load.decode())

def DNSFilter(p):
    return DNS in p and p[DNS].opcode==0 and DNSQR in p and p[DNSQR].qname.startswith(b'www.google.com')

def DNSPrint(pack):
    print(pack[DNSQR].qname.decode())

p = sniff(iface=r"\Device\NPF_Loopback",count=2, lfilter=HTTPFilter, prn=HTTPrint)

