import socket


PORT = 1450
SERVER_NAME = "MyServer"

def send_response(sock, response):
    """
    Send a response to the client
    First send 4 bytes that contain the length of the message,
    then add 5 layers
    and last sends the response
    """


    data = response.encode()

    length = str(len(data)).zfill(4)

    sock.sendall(length.encode())
    sock.sendall(data)


server_sock = socket.socket()
server_sock.bind(("0.0.0.0", PORT))
server_sock.listen(3)