from scapy.all import *
myface = conf.route.route("8.8.8.8")[0]


def HTTPFilter(p):
    return TCP in p and Raw in p  and p[Raw].load.startswith(b'GET')


def HTTPrint(p):
    print("hello")
    print(p[Raw])
    #print(p[Raw].load.decode())

def DNSFilter(p):
    return DNS in p and p[DNS].opcode==0 and DNSQR in p and p[DNSQR].qname.startswith(b'www.google.com')

def DNSPrint(pack):
    print(pack[DNSQR].qname.decode())

p = sniff(iface=myface,count=10, lfilter=HTTPFilter, prn=HTTPrint)



