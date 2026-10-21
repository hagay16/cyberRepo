import socket
import platform
import os
import subprocess

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




server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 8080)) #if 80 not work do 8080
server_socket.listen(3)


no_access = ["cowboy.png"]

redirects = {"page1.txt": "page2.txt"}


while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr[0]} - connected")



    try:
        data = client_socket.recv(1024).decode()

    except Exception as e:
        print(f"error in receive {str(e)}")
        break
    else:
        print(data)

    url = getURL(data)


    if url:
        if url in redirects:
            url = redirects[url]

        if url == "server":
            ans = "HTTP/1.1 500 Internal Server Error\r\nContent-Length: 0\r\n\r\n"
            file_info = None

        elif url in no_access:
            ans = "HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n"
            file_info = None



        else :
            file_info, file_len = getData(url)

            if file_info is None:
                ans = f"HTTP/1.1 404 Not Found\r\nContent-Length:0\r\n\r\n"
            else:
                ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(file_len)}\r\n\r\n"


        try:
            client_socket.send(ans.encode())
            client_socket.send(file_info)
        except Exception as e:
            print(f"error in receive {str(e)}")

    client_socket.close()

server_socket.close()