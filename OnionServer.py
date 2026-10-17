import socket

PORT = 1450


def recv_big_data(sock, data_len):
    """
    Receives data from a socket in chunks.

    :param sock: client socket
    :param data_len: amount of data to receive
    :return: received bytes
    """
    data = b""

    while len(data) < data_len:
        amount_left = data_len - len(data)

        if amount_left > 1024:
            chunk = sock.recv(1024)
        else:
            chunk = sock.recv(amount_left)

        if chunk == b"":
            raise ConnectionError("client disconnected")

        data += chunk

    return data


def layer1(data):
    """
    Removes layer 1.

    :param data: received data
    :return: data without layer 1
    """
    return data[:-len("layer1" * 10)]


def layer2(data):
    """
    Removes layer 2.

    :param data: received data
    :return: data without layer 2
    """
    return data[:-len("-----" * 10)]


def layer3(data):
    """
    Removes layer 3.

    :param data: received data
    :return: data without layer 3
    """
    return data[:-len("1111111" * 10)]


def layer4(data):
    """
    Removes layer 4.

    :param data: received data
    :return: data without layer 4
    """
    return data[:-len("HaHa" * 10)]


def layer5(data):
    """
    Removes layer 5.

    :param data: received data
    :return: data without layer 5
    """
    return data[:-len("last" * 10)]


server_sock = socket.socket()
server_sock.bind(("0.0.0.0", PORT))
server_sock.listen(3)

print("Server is running")

while True:
    client_socket, addr = server_sock.accept()
    print(f"{addr[0]} connected")

    while True:
        try:
            length_data = client_socket.recv(4).decode()
        except Exception as e:
            print(f"error receiving data: {str(e)}")
            break

        if length_data == "":
            break

        message_len = int(length_data)

        try:
            message = client_socket.recv(message_len).decode()
        except Exception as e:
            print(f"communication error: {str(e)}")
            break

        message = layer5(message)
        message = layer4(message)
        message = layer3(message)
        message = layer2(message)
        message = layer1(message)

        print(f"message: {message}")

    client_socket.close()
    print(f"{addr[0]} disconnected")