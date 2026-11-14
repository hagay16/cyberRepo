import socket

def recv_response(sock):
    """
    Receive a response from the server.
    first receives 4 bytes of the response length,
    then receives the response itself.
    return: response from server
    """
    length = int(sock.recv(4).decode())
    data = sock.recv(length).decode()

    return data

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

def check_next(choice,object):
    my_sock = socket.socket()

    try:
        my_sock.connect(("127.0.0.1", 1451))
    except Exception as e:
        my_sock.close()
        exit(f"server is down - try again later: {str(e)}")
    my_sock.send(str(len(choice)).zfill(8).encode())
    my_sock.send(choice.encode())
    my_sock.send(str(len(object)).zfill(10).encode())
    my_sock.send(object.encode())

    try:
        response = recv_response(my_sock)
    except Exception as e:
        print(f"error receiving data: {str(e)}")

    my_sock.close()
    return response

server_sock = socket.socket()
server_sock.bind(("0.0.0.0", 1450))
server_sock.listen(3)

IP_to_HostName = {"2.2.2.2":"TwoPointTwo","3.3.3.3":"3Website"}
HostName_to_IP = {"TwoPointTwo":"2.2.2.2","3Website":"3.3.3.3"}

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
            if data in IP_to_HostName:
                response = IP_to_HostName[data]
                print(f"your host name for ip: {data}, is: {IP_to_HostName[data]}")
            else:
                print("ip was not found in local dns, looking in central dns...")
                # here look in central dns
                response = check_next(choice, data)
                IP_to_HostName[data] = response
        else:
            if data in HostName_to_IP:
                response = HostName_to_IP[data]
                print(f"your ip for host name: {data}, is: {HostName_to_IP[data]}")
            else:
                print("host name was not found in local dns, looking in central dns...")
                # here look in central dns
                response = check_next(choice, data)
                HostName_to_IP[data] = response

        try:
            send_response(client_sock, response)
        except Exception as e:
            print(f"error sending data: {str(e)}")
            break
        print(f"{addr[0]} - disconnected")
        client_sock.close()
        break
    client_sock.close()



