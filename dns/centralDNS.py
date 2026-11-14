import socket

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
server_sock.bind(("0.0.0.0", 1451))
server_sock.listen(3)

IP_to_HostName = {"67.67.67.67":"sixseven","6.7.8.9":"seven89"}
HostName_to_IP = {"sixseven":"67.67.67.67","seven89":"1.2.3.4"}

while True:
    client_sock, addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    while True:


        try:
            choice_len = client_sock.recv(8).decode()
            choice = client_sock.recv(int(choice_len)).decode()
            data_len = client_sock.recv(10).decode()
            data = client_sock.recv(int(data_len)).decode()
        except Exception as e:
            print(f"error receiving data: {str(e)}")
            break

        if choice == "ip":
            response = IP_to_HostName[data]
            print(f"your host name for ip: {data}, is: {IP_to_HostName[data]}")
        else:
            response = HostName_to_IP[data]
            print(f"your ip for host name: {data}, is: {HostName_to_IP[data]}")

        try:
            send_response(client_sock, response)
        except Exception as e:
            print(f"error sending data: {str(e)}")
            break
        print(f"{addr[0]} - disconnected")
        client_sock.close()
        break
    client_sock.close()
