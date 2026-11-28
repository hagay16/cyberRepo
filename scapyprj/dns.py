from scapy.all import *



def DNSFilter(p):
    return DNS in p and p[DNS].opcode==0 and p[DNS].qr == 1 and DNSRR in p and p[IP].dst == get_if_addr(conf.iface)

def DNSPrint(pack):
    for answer in pack[DNS].an:
        if answer.type == 1:
            print(answer.rdata)



sniff(count=10, lfilter=DNSFilter, prn=DNSPrint)