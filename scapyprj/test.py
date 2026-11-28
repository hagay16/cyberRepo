from scapy.all import *

packets = sniff(count=2)
packets.summary()