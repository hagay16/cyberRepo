import socket


PORT = 1450

def layer1(data):
    """add first layer to data: layer 1 = 'layer1' ten times"""
    for t in range(10):
        data += 'layer1'

def layer2(data):
    for t in range(10):
        data +=


my_sock = socket.socket()

try:
    my_sock.connect(("127.0.0.1", PORT))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again later: {str(e)}")



while True:
    command = input("Enter message or exit")
    command.upper()
    if command == "EXIT" :
        break



    #delayer








my_sock.close()
print("goodbye")