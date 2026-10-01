import socket

from PIL import Image


SERVER_IP = "127.0.0.1"
PORT = 1450


def recv_exact(sock, amount):
    data = b""

    while len(data) < amount:
        chunk = sock.recv(amount - len(data))

        if chunk == b"":
            raise ConnectionError("server disconnected")

        data += chunk

    return data


def recv_message(sock):
    length = int(
        recv_exact(sock, 8).decode()
    )

    return recv_exact(sock, length)


def send_message(sock, data):
    if isinstance(data, str):
        data = data.encode()

    length = str(len(data)).zfill(8).encode()

    sock.sendall(length)
    sock.sendall(data)


def print_menu():
    print()
    print("1 - screenshot")
    print("2 - copy text to server clipboard")
    print("3 - paste server clipboard")
    print("4 - run program")
    print("5 - show folder contents")
    print("6 - delete file")
    print("7 - copy file")
    print("8 - exit")
    print()


client_socket = socket.socket()

try:
    client_socket.connect(
        (SERVER_IP, PORT)
    )

except Exception as e:
    print(
        f"server is down: {str(e)}"
    )

    client_socket.close()
    exit()


while True:
    print_menu()

    choice = input(
        "choose command: "
    )

    try:
        # Screenshot
        if choice == "1":
            send_message(
                client_socket,
                "SCREEN"
            )

            image_data = recv_message(
                client_socket
            )

            with open("screenshot.jpg", "wb") as f:
                f.write(image_data)

            image = Image.open("screenshot.jpg")
            image.show()

            print("screenshot received")


        # Copy to clipboard
        elif choice == "2":
            text = input(
                "text to copy: "
            )

            send_message(
                client_socket,
                "COPY " + text
            )

            response = recv_message(
                client_socket
            ).decode()

            print(response)


        # Paste clipboard
        elif choice == "3":
            send_message(
                client_socket,
                "PASTE"
            )

            response = recv_message(
                client_socket
            ).decode()

            print(
                f"server clipboard: {response}"
            )


        # Run program
        elif choice == "4":
            program = input(
                "program (google/calc): "
            )

            send_message(
                client_socket,
                "RUN " + program
            )

            response = recv_message(
                client_socket
            ).decode()

            print(response)


        # List folder
        elif choice == "5":
            folder = input(
                "enter full folder path: "
            )

            send_message(
                client_socket,
                "DIR " + folder
            )

            response = recv_message(
                client_socket
            ).decode()

            print("folder contents:")
            print(response)


        # Delete file
        elif choice == "6":
            file_path = input(
                "enter full file path to delete:  "
            )

            send_message(
                client_socket,
                "DELETE " + file_path
            )

            response = recv_message(
                client_socket
            ).decode()

            print(response)


        # Copy file
        elif choice == "7":
            source = input(
                "enter full source file path: "
            )

            destination = input(
                "enter full destination file path: "
            )

            command = (
                "COPYFILE "
                + source
                + "|"
                + destination
            )

            send_message(
                client_socket,
                command
            )

            response = recv_message(
                client_socket
            ).decode()

            print(response)


        # Exit
        elif choice == "8":
            send_message(
                client_socket,
                "EXIT"
            )

            break


        else:
            print("invalid choice")


    except Exception as e:
        print(
            f"communication error: {str(e)}"
        )
        break


client_socket.close()

print("bye bye")