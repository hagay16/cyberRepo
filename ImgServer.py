import socket
import os
import platform
import subprocess


PORT = 1450
SAVE_FOLDER = "received_images"


def recv_exact(sock, amount):
    data = b""

    while len(data) < amount:
        chunk = sock.recv(amount - len(data))

        if chunk == b"":
            raise ConnectionError("Client disconnected")

        data += chunk

    return data


def open_image(file_path):
    system = platform.system()

    if system == "Windows":
        os.startfile(file_path)

    elif system == "Linux":
        subprocess.Popen(["xdg-open", file_path])



def recv_image_data(client_socket, file_name, file_data_len):
    file_data = recv_exact(client_socket, file_data_len)

    file_name = os.path.basename(file_name)

    os.makedirs(SAVE_FOLDER, exist_ok=True)

    file_path = os.path.join(SAVE_FOLDER, file_name)

    with open(file_path, "wb") as f:
        f.write(file_data)

    print(f"Image saved: {file_path}")

    open_image(file_path)


server_soc = socket.socket()
server_soc.bind(("0.0.0.0", PORT))
server_soc.listen(3)

print("Server is running")


while True:
    client_socket, addr = server_soc.accept()
    print(f"{addr[0]} - connected")

    while True:
        try:
            file_name_len_data = client_socket.recv(2)

            if file_name_len_data == b"":
                break

            file_name_len = int(file_name_len_data.decode())

            file_name = recv_exact(
                client_socket,
                file_name_len
            ).decode()

            file_data_len = int(
                recv_exact(client_socket, 6).decode()
            )

            recv_image_data(
                client_socket,
                file_name,
                file_data_len
            )

        except Exception as e:
            print(
                f"Client {addr[0]} disconnected due to {str(e)}"
            )
            break

    client_socket.close()
    print(f"{addr[0]} - disconnected")