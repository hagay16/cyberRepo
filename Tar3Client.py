import socket

mysock = socket.socket()

try:
    mysock.connect(("127.0.0.1", 1450))
except Exception as e:
    mysock.close()
    exit(f"server is down, try again later: {str(e)}")

while True:
    msg = input("enter message to send or q to finish: ")

    if msg.lower() == "q":
        break

    try:
        mysock.sendall(msg.encode())

        data = mysock.recv(1024).decode()
        print(f"server sent - {data}")

    except Exception as e:
        print(f"error in receiving or sending data: {str(e)}")
        break

mysock.close()
print("goodbye")