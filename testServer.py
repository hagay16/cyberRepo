import socket
import random
import time
server_sock = socket.socket()
server_sock.bind(("0.0.0.0" , 1450))
server_sock.listen(3)

while True:
    #server wait for clients

    client_sock,addr = server_sock.accept()
    print(f"{addr[0]} - connected")

    while True:
        #handle one client

        try:
            data = client_sock.recv(4).decode()
            if data == "":
                break
            print(f"getting data - {data}")
            if data.lower() == "name":
                name = "UriLindner"
                nameLen = str(len(name)).zfill(2)
                client_sock.send(nameLen.encode())
                client_sock.send(name.encode())

            elif data.lower() == "rand":
                randomNumber = random.randint(1, 11)
                numLen = str(len(str(randomNumber))).zfill(2)
                client_sock.send(numLen.encode())
                client_sock.send(str(randomNumber).encode())

            elif data.lower() == "time":
                currentTime = time.ctime()
                timeLen = str(len(currentTime)).zfill(2)
                client_sock.send(timeLen.encode())
                client_sock.send(currentTime.encode())

            elif data.lower() == "exit":
                print(f"{addr[0]} - disconnected")
                msg = "goodbye"
                msgLen = str(len(msg)).zfill(2)
                client_sock.send(msgLen.encode())
                client_sock.send(msg.encode())
                client_sock.close()
                break

            else:
                print(f"{addr[0]} - kick out")
                client_sock.close()
                break

        except Exception as e:
            print(f"error in recv/send {str[e]}")
            client_sock.close()
            break