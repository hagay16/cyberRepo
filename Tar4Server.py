import socket
import os
import platform
from Tar4Functions import (
    recv_big_data,
    copy_to_clipboard,
    paste_from_clipboard,
    run_program,
    get_folder_content,
    delete_file,
    copy_file,
    send_screen
)

HOST = "0.0.0.0"
PORT = 1450

BASE_FOLDER = os.path.abspath("server_files")




server_socket = socket.socket()
server_socket.bind((HOST, PORT))
server_socket.listen(3)

print("server is running")

while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr[0]} connected")

    while True:
        try:
            command = client_socket.recv(1).decode()
        except Exception as e:
            print(f"receive error: {str(e)}")
            break

        if command == "":
            break

        print(f"command: {command}")

        if command == "1":
            try:
                send_screen(client_socket)
            except Exception as e:
                print(f"screenshot error: {str(e)}")
                break

        elif command == "2":
            try:
                text_len = int(client_socket.recv(4).decode())
                text = recv_big_data(client_socket, text_len).decode()
                success = copy_to_clipboard(text)
                client_socket.sendall(("1" if success else "0").encode())
            except Exception as e:
                print(f"clipboard error: {str(e)}")
                break

        elif command == "3":
            try:
                text = paste_from_clipboard()
                text_data = text.encode()
                text_len = str(len(text_data)).zfill(4)

                client_socket.sendall(text_len.encode())
                client_socket.sendall(text_data)
            except Exception as e:
                print(f"clipboard error: {str(e)}")
                break



        elif command == "4":
            try:
                program_len = int(client_socket.recv(2).decode())
                program = client_socket.recv(program_len).decode()

                response = run_program(program)

                client_socket.sendall(str(len(response)).zfill(2).encode())
                client_socket.sendall(response.encode())
            except Exception as e:
                print(f"program error: {str(e)}")
                break

        elif command == "5":
            try:
                path_len = int(client_socket.recv(3).decode())
                folder = client_socket.recv(path_len).decode()
                result = get_folder_content(folder).encode()

                result_len = str(len(result)).zfill(5)

                client_socket.sendall(result_len.encode())
                client_socket.sendall(result)
            except Exception as e:
                print(f"folder error: {str(e)}")
                break

        elif command == "6":
            try:
                path_len = int(client_socket.recv(3).decode())
                file_path = client_socket.recv(path_len).decode()
                success = delete_file(file_path)

                client_socket.sendall(("1" if success else "0").encode())
            except Exception as e:
                print(f"delete error: {str(e)}")
                break

        elif command == "7":
            try:
                source_len = int(client_socket.recv(3).decode())
                source = client_socket.recv(source_len).decode()

                destination_len = int(client_socket.recv(3).decode())
                destination = client_socket.recv(destination_len).decode()

                success = copy_file(source, destination)

                client_socket.sendall(("1" if success else "0").encode())
            except Exception as e:
                print(f"copy file error: {str(e)}")
                break

        elif command == "8":
            break

        else:
            # illegal command disconnect
            print(f"illegal command from {addr[0]}")
            break

    client_socket.close()
    print(f"{addr[0]} disconnected")