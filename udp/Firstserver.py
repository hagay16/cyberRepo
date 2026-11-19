import socket

server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0",2010))

while True:
    data,client_address = server_socket.recvfrom(1024)
    print(f"client sent: {data.decode()}")
    try:
        server_socket.sendto(f"Hello {data.decode()}".encode(),client_address)
    except Exception as e:
        pass

server_socket.close()