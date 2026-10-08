import socket


PORT = 1450





my_sock = socket.socket()

try:
    my_sock.connect(("127.0.0.1", PORT))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again later: {str(e)}")



while True:
    command = input("Enter message or exit")









my_sock.close()
print("goodbye")