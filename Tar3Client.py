import socket


PORT = 1450
VALID_COMMANDS = ["TIME", "NAME", "RAND", "EXIT"]

mysock = socket.socket()

try:
    mysock.connect(("127.0.0.1", PORT))
except Exception as e:
    mysock.close()
    exit(f"server is down, try again later: {str(e)}")


while True:
    msg = input("Enter TIME, NAME, RAND or EXIT: ").upper()

    # Do not waste the server's time with illegal commands
    if msg not in VALID_COMMANDS:
        print("invalid command")
        continue

    try:
        # Every valid command is exactly 4 bytes
        mysock.sendall(msg.encode())

        if msg == "EXIT":
            break

        # First receive 4 bytes containing response length
        length_data = mysock.recv(4).decode()
        response_length = int(length_data)

        # Then receive the actual response
        data = mysock.recv(response_length).decode()

        print(f"server sent - {data}")

    except Exception as e:
        print(f"error in receiving or sending data: {str(e)}")
        break


mysock.close()
print("goodbye")