import socket

PORT = 1450
SERVER_IP = "127.0.0.1"


def layer1(data):
    """
    Adds layer 1 to the data.

    :param data: original data
    :return: data with layer 1
    """
    return data + "layer1" * 10


def layer2(data):
    """
    Adds layer 2 to the data.

    :param data: data from previous layer
    :return: data with layer 2
    """
    return data + "-----" * 10


def layer3(data):
    """
    Adds layer 3 to the data.

    :param data: data from previous layer
    :return: data with layer 3
    """
    return data + "1111111" * 10


def layer4(data):
    """
    Adds layer 4 to the data.

    :param data: data from previous layer
    :return: data with layer 4
    """
    return data + "HaHa" * 10


def layer5(data):
    """
    Adds layer 5 to the data.

    :param data: data from previous layer
    :return: data with layer 5
    """
    return data + "last" * 10


my_sock = socket.socket()

try:
    my_sock.connect((SERVER_IP, PORT))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again later: {str(e)}")


while True:
    message = input("Enter message or exit: ")

    if message.lower() == "exit":
        break

    message = layer1(message)
    message = layer2(message)
    message = layer3(message)
    message = layer4(message)
    message = layer5(message)

    data = message.encode()
    length = str(len(data)).zfill(4).encode()

    try:
        my_sock.send(length)
        my_sock.send(data)
    except Exception as e:
        print(f"communication error: {str(e)}")
        break


my_sock.close()
print("goodbye")