import socket
import os
import platform
import subprocess
from Tar4Functions import recv_big_data


PORT = 1450
SAVE_FOLDER = "received_images"

SYSTEMNAME = platform.system()

def open_image(file_path):
    """
    Opens an image using the default image viewer.
    """
    if SYSTEMNAME == "Windows":
        os.startfile(file_path)
    else:
        subprocess.Popen(["xdg-open", file_path])


def recv_image(client_socket, file_name, file_data_len):
    """
    Receives an image from the client, saves it and opens it
    """
    file_data = recv_big_data(client_socket, file_data_len)

    os.makedirs(SAVE_FOLDER, exist_ok=True)
    file_path = os.path.join(SAVE_FOLDER, os.path.basename(file_name))

    with open(file_path, "wb") as f: #open destination file and write image bytes
        f.write(file_data)

    print(f"image saved: {file_path}")
    open_image(file_path)


server_socket = socket.socket()
server_socket.bind(("0.0.0.0", PORT))
server_socket.listen(3)

print("server is running")

while True:
    client_socket, addr = server_socket.accept()
    print(f"{addr[0]} connected")

    while True:
        try:
            file_name_len_data = client_socket.recv(2)
        except Exception as e:
            print(f"receive error: {str(e)}")
            break

        if file_name_len_data == b"":
            break

        try:
            file_name_len = int(file_name_len_data.decode())
            file_name = client_socket.recv(file_name_len).decode()
            file_data_len = int(client_socket.recv(6).decode())
            recv_image(client_socket, file_name, file_data_len)
        except Exception as e:
            print(f"image receive error: {str(e)}")
            break

    client_socket.close()
    print(f"{addr[0]} disconnected")