from scapy.all import *

def HTTPFilter(p):
    return TCP in p and Raw in p and p[Raw].load.startswith(b"GET")

def HTTPrint(p):
    print(p[Raw].load.decode())

def HTTPrintURL(p):
    data = p[Raw].load.decode()
    url = data.split(" ")[1]

    for line in data.split("\r\n"):
        if line.startswith("Host: "):
            host = line[6:]
            print("http://" + host + url)
            break


p = sniff(count=10,lfilter=HTTPFilter,prn=HTTPrintURL)