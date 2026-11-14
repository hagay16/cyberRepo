import os
import socket

SERVER_IP = "127.0.0.0"

def send_post(url, body):
    """
    Send an HTTP POST request to the server.
    :param url: Request URL
    :param body: Request body as bytes
    :return: None
    """
    request = (f"POST {url} HTTP/1.1\r\nHost: {SERVER_IP}\r\nContent-Length: {len(body)}\r\nConnection: close\r\n\r\n")

    client_socket = socket.socket()

    try:
        client_socket.connect((SERVER_IP, 8080))
        client_socket.sendall(request.encode() + body)
    except Exception as e:
        print(f"server is down: {str(e)}")

def send_secret():
    """
    Get a secret message and send it to the server.
    """
    message = input("Enter secret message: ")
    body = message.encode()
    send_post("/httpPart3Server?secret",body)

def send_picture():
    """
    Read a picture from a file and send it to the server.
    """
    picture_path = input("Enter picture path: ")

    if not os.path.isfile(picture_path):
        print("Picture does not exist")
        return

    picture_name = os.path.basename(picture_path)

    with open(picture_path, "rb") as file:
        body = file.read()

    url = f'/httpPart3Server?img_name={picture_name}'
    send_post(url, body)




while True:

    command = input("enter secret, picture or exit: ").lower()

    if command == "exit":
        print("goodbye")
        break
    elif command == "secret":
        send_secret()
    elif command == "picture":
        send_picture()
    else:
        print("invalid command")
