import socket
my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
    data2send = input("enter message to send or exit: ")
    if data2send.lower() == 'exit':
        break
    try:
        my_socket.sendto(data2send.encode(),('127.0.0.1',2010))
    except Exception as e:
        break
    data,remote_address = my_socket.recvfrom(1024)
    print(f"The sever sent:{data.decode()}")