import socket

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1450))
server_sock.listen(3)

while True:
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:
            data = client_sock.recv(1024).decode()

            if data == "":
                break

            print(f"getting data - {data}")

            client_sock.sendall(data.encode())

        except Exception as e:
            print(f"error in recv/send {str(e)}")
            break

    print(f"{addr[0]} - disconnected")
    client_sock.close()