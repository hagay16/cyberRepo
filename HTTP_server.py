import socket

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
    return url[1:]



server_socket = socket.socket()
server_socket.bind(("0.0.0.0", 80)) #if 80 not work do 8080
server_socket.listen(3)


while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr[0]} - connected")

    try:
        data = client_socket.recv(1024).decode()
    except Exception as e:
        print(f"error in receive {str(e)}")
    else:
        print(data)

    url = getURL(data)


    if url:
        ans = f"HTTP/1.1 200 OK\r\nContent-Length: {str(len(url))}\r\n\r\n{url}"

        try:
            data = client_socket.send(ans.encode())
        except Exception as e:
            print(f"error in receive {str(e)}")
