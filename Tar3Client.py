import socket


PORT = 1450
VALID_COMMANDS = ["TIME", "NAME", "RAND", "EXIT"]


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


my_sock = socket.socket()

try:
    my_sock.connect(("127.0.0.1", PORT))
except Exception as e:
    my_sock.close()
    exit(f"server is down - try again later: {str(e)}")


while True:
    command = input(
        "enter TIME, NAME, RAND or EXIT: "
    ).upper()

    # Validation is outside try
    if command not in VALID_COMMANDS:
        print("invalid command - try again")
        continue

    try:
        my_sock.sendall(command.encode())
    except Exception as e:
        print(f"error sending data: {str(e)}")
        break

    if command == "EXIT":
        break

    try:
        response = recv_response(my_sock)
    except Exception as e:
        print(f"error receiving data: {str(e)}")
        break

    print(response)


my_sock.close()
print("goodbye")