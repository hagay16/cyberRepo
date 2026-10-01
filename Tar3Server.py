import socket
import time
import random


PORT = 1450
SERVER_NAME = "MyServer"


def send_response(sock, response):
    data = response.encode()


    length = str(len(data)).zfill(4)

    sock.sendall(length.encode())
    sock.sendall(data)


server_sock = socket.socket()
server_sock.bind(("0.0.0.0", PORT))
server_sock.listen(3)

print("server is running")

while True:
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:
            # Every request is exactly 4 bytes
            data = client_sock.recv(4).decode()

            if data == "":
                break

            print(f"getting command - {data}")

            if data == "TIME":
                response = time.strftime("%H:%M:%S")
                send_response(client_sock, response)

            elif data == "NAME":
                response = SERVER_NAME
                send_response(client_sock, response)

            elif data == "RAND":
                response = str(random.randint(1, 11))
                send_response(client_sock, response)

            elif data == "EXIT":
                print(f"{addr[0]} requested disconnect")
                break

        except Exception as e:
            print(f"error in recv/send: {str(e)}")
            break

    print(f"{addr[0]} - disconnected")
    client_sock.close()