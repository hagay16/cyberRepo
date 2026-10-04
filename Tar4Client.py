import socket
from PIL import Image
from Tar4Functions import (
    recv_big_data
)

SERVER_IP = "127.0.0.1"
PORT = 1450

def print_menu():
    """
    Prints the available commands.

    :return: None
    """
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
    client_socket.connect((SERVER_IP, PORT))
except Exception as e:
    print(f"server is down: {str(e)}")
    client_socket.close()
    exit()


while True:
    print_menu()
    choice = input("choose command: ")

    if choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        print("invalid choice")
        continue

    if choice == "1":
        try:
            client_socket.sendall(b"1")

            image_len = int(client_socket.recv(7).decode())
            image_data = recv_big_data(client_socket, image_len)

            with open("screenshot.jpg", "wb") as f:
                f.write(image_data)

            image = Image.open("screenshot.jpg")
            image.show()

            print("screenshot received")

        except Exception as e:
            print(f"communication error: {str(e)}")
            break

    elif choice == "2":
        text = input("text to copy: ")
        text_data = text.encode()
        text_len = str(len(text_data)).zfill(4)

        try:
            client_socket.sendall(b"2")
            client_socket.sendall(text_len.encode())
            client_socket.sendall(text_data)

            result = client_socket.recv(1).decode()

        except Exception as e:
            print(f"communication error: {str(e)}")
            break

        if result == "1":
            print("copy succeeded")
        else:
            print("copy failed")

    elif choice == "3":
        try:
            client_socket.sendall(b"3")

            text_len = int(client_socket.recv(4).decode())
            text = recv_big_data(client_socket, text_len).decode()

        except Exception as e:
            print(f"communication error: {str(e)}")
            break

        print(f"server clipboard: {text}")

    elif choice == "4":
        program = input("program (google/calc): ")

        program_data = program.encode()
        program_len = str(len(program_data)).zfill(2)

        try:
            client_socket.sendall(b"4")
            client_socket.sendall(program_len.encode())
            client_socket.sendall(program_data)

            response_len = int(client_socket.recv(2).decode())
            response = client_socket.recv(response_len).decode()
            print(response)

        except Exception as e:
            print(f"communication error: {str(e)}")
            break





    elif choice == "5":
        folder = input("enter full folder path: ")
        folder_data = folder.encode()
        folder_len = str(len(folder_data)).zfill(3)

        try:
            client_socket.sendall(b"5")
            client_socket.sendall(folder_len.encode())
            client_socket.sendall(folder_data)

            result_len = int(client_socket.recv(5).decode())
            result = recv_big_data(client_socket, result_len).decode()

        except Exception as e:
            print(f"communication error: {str(e)}")
            break

        print("folder contents:")
        print(result)

    elif choice == "6":
        file_path = input("enter full file path to delete: ")
        path_data = file_path.encode()
        path_len = str(len(path_data)).zfill(3)

        try:
            client_socket.sendall(b"6")
            client_socket.sendall(path_len.encode())
            client_socket.sendall(path_data)

            result = client_socket.recv(1).decode()

        except Exception as e:
            print(f"communication error: {str(e)}")
            break

        if result == "1":
            print("file deleted successfully")
        else:
            print("file delete failed")

    elif choice == "7":
        source = input("enter full source file path: ")
        destination = input("enter full destination file path: ")

        source_data = source.encode()
        destination_data = destination.encode()

        source_len = str(len(source_data)).zfill(3)
        destination_len = str(len(destination_data)).zfill(3)

        try:
            client_socket.sendall(b"7")

            client_socket.sendall(source_len.encode())
            client_socket.sendall(source_data)

            client_socket.sendall(destination_len.encode())
            client_socket.sendall(destination_data)

            result = client_socket.recv(1).decode()

        except Exception as e:
            print(f"communication error: {str(e)}")
            break

        if result == "1":
            print("file copied successfully")
        else:
            print("file copy failed")

    elif choice == "8":
        try:
            client_socket.sendall(b"8")
        except Exception as e:
            print(f"communication error: {str(e)}")

        break


client_socket.close()
print("bye bye")