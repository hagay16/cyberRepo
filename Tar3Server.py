import socket
import time
import random


PORT = 1450
SERVER_NAME = "MyServer"


def send_response(sock, response):
    """
    Send a response to the client
    First send 4 bytes that contain the length of the message,
    then sends the response
    """
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
            data = client_sock.recv(4).decode()
        except Exception as e:
            print(f"error receiving data: {str(e)}")
            break

        # client disconnected
        if data == "":
            break

        print(f"getting command - {data}")

        # Handle the command outside the try
        if data == "TIME":
            response = time.strftime("%H:%M:%S")

        elif data == "NAME":
            response = SERVER_NAME

        elif data == "RAND":
            response = str(random.randint(1, 11))

        elif data == "EXIT":
            print(f"{addr[0]} requested disconnect")
            break

        else:
            # ilegal command disconnect
            print(f"illegal command from {addr[0]}: {data}")
            break

        # Send the response only once
        try:
            send_response(client_sock, response)
        except Exception as e:
            print(f"error sending data: {str(e)}")
            break

    print(f"{addr[0]} - disconnected")
    client_sock.close()