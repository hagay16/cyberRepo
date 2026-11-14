import socket
import platform
import os


SYSTEMNAME = platform.system()

def getURL(ans):
    """
    return the url from the client request
    :param ans: the request
    :return: the url
    """
    url = None
    line1 = ans.split('\r\n')[0]
    params = line1.split(' ')
    if len(params) == 3 and params[0] == 'GET' and params[2] == "HTTP/1.1":
        url = params[1]
    if url == "/":
        url = "/My_html.html"
    return url[1:]

def getData(url):
    """
    Read the requested file.
    :param url: File path
    :return: File content and length
    """
    file_info = None
    file_len = None

    if os.path.isfile(url):
        with open(url, 'rb') as file:
            file_info = file.read()
            file_len = len(file_info)

    return file_info, file_len

def check_post_packet(data):
    valid = False
    lines = data.split('\r\n')[0]
    params = lines.split(' ')
    if len(params) == 3 and params[0] == 'POST' and params[2] == 'HTTP/1.1' and params[1] == '/httpPart3Server?secret' or params[1].startswith('/httpPart3Server?img_name='):
        valid = True
    return valid

def post_data(header, body):
    lines = header.split('\r\n')[0]
    params = lines.split(' ')
    url = params[1]
    return url, body


def receive_post(client_socket):
    data = b''


    while b'\r\n\r\n' not in data:
        try:
            chunk = client_socket.recv(1024)
        except OSError as e:
            print(f"Error in receive: {e}")
            raise

        if not chunk:
            raise ConnectionError("Client disconnected")
        data += chunk

    headers, body = data.split(b'\r\n\r\n', 1)
    headers = headers.decode()

    # Find Content-Length
    content_length = None

    for line in headers.split('\r\n'):
        if line.lower().startswith('content-length:'):
            content_length = int(line.split(':', 1)[1].strip())

    if content_length is None:
        if headers.startswith("GET "):
            content_length = 0
        else:
            raise ValueError("Missing Content-Length")

    if content_length < 0:
        raise ValueError("Invalid Content-Length")

    # Receive the remaining body
    while len(body) < content_length:
        try:
            chunk = client_socket.recv(1024)
        except OSError as e:
            print(f"Error in receive: {e}")
            raise
        if not chunk:
            raise ConnectionError("Incomplete body")
        body += chunk

    return headers, body[:content_length]

def send_image(client_socket, url):
    picture_name = os.path.basename(url.split("=", 1)[1])

    if not picture_name or picture_name in (".", ".."):
        return

    if os.path.isfile(picture_name):
        with open(picture_name, "rb") as file:
            img_data = file.read()

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: image/jpeg\r\n"
            f"Content-Length: {len(img_data)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )

        client_socket.sendall(response.encode() + img_data)

server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8080)) #if 80 not work do 8080
server_socket.listen(3)


while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr[0]} - connected")

    headers, body = receive_post(client_socket)

    if headers.startswith("GET"):
        url = getURL(headers)

        if url.startswith("/image?img-name="):
            send_image(client_socket, url)

    
    elif headers.startswith("POST "):
        if check_post_packet(headers):
            print("received data")
            url, data = post_data(headers, body)
            if url == "/httpPart3Server?secret":
                msg =data.decode()
                print(f"the secret message is {msg}")
                with open("secret_messages.txt", "a") as file:
                    file.write(msg + '\n')
            elif url.startswith("/httpPart3Server?img_name="):
                picture_name = os.path.basename(url.split("=")[1])
                with open(picture_name, "wb") as file:
                    file.write(data)
                print(f"Picture {picture_name} saved")
        else:
            print("Invalid POST request")



    client_socket.close()
    print("Disconnected")

server_socket.close()