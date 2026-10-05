import socket

mysock = socket.socket()

try:
    mysock.connect(("192.168.4.75", 1450))#
except Exception as e:
    mysock.close()
    exit(f"server is down try again later {str(e)}")


while True:
    msg = input("enter message to send or exit to finish: ")
    if len(msg) == 4:

        try:
            mysock.send(msg.encode())
            data_length = mysock.recv(2).decode()
            data = mysock.recv(int(data_length)).decode()
            print(f"server send - {data}")
            if msg.lower() == "exit":
                break
        except Exception as e:
            print(f"error in receiving or sending data {str(e)}")
            break
    else:
        print("the length of the message is wrong, pls try another message")


mysock.close()