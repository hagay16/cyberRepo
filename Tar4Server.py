import socket
import os
import shutil
import subprocess
import pyperclip
import platform


HOST = "0.0.0.0"
PORT = 1450

BASE_FOLDER = os.path.abspath("server_files")

if platform.system() == "Windows":
    ALLOWED_PROGRAMS = {
        "calc": "calc.exe",
        "google": "chrome.exe"
    }
else:
    ALLOWED_PROGRAMS = {
        "calc": "gnome-calculator",
        "google": "google-chrome"
    }


def recv_exact(sock, amount):
    data = b""

    while len(data) < amount:
        chunk = sock.recv(amount - len(data))

        if chunk == b"":
            raise ConnectionError("client disconnected")

        data += chunk

    return data


def recv_message(sock):
    # first 8 bytes = message length
    length = int(recv_exact(sock, 8).decode())

    return recv_exact(sock, length)


def send_message(sock, data):
    if isinstance(data, str):
        data = data.encode()

    length = str(len(data)).zfill(8).encode()

    sock.sendall(length)
    sock.sendall(data)


def safe_path(path):
    """
    Converts a path to a path inside BASE_FOLDER.
    Prevents access outside the assignment folder.
    """

    full_path = os.path.abspath(
        os.path.join(BASE_FOLDER, path)
    )

    if not full_path.startswith(BASE_FOLDER):
        raise ValueError("invalid path")

    return full_path


def handle_screen(client_socket):
    screen_path = os.path.join(
        BASE_FOLDER,
        "screen.png"
    )

    subprocess.run(
        ["gnome-screenshot", "-f", screen_path],
        check=True
    )

    with open(screen_path, "rb") as f:
        image_data = f.read()

    send_message(client_socket, image_data)

def handle_copy(text):
    pyperclip.copy(text)

    # verify that the clipboard contains it
    if pyperclip.paste() == text:
        return "copy succeeded"

    return "copy failed"


def handle_paste():
    return pyperclip.paste()


def handle_run(program):
    program = program.lower()

    if program not in ALLOWED_PROGRAMS:
        return "program is not allowed"

    try:
        subprocess.Popen([ALLOWED_PROGRAMS[program]])
        return "program started successfully"

    except Exception as e:
        return f"failed to start program: {str(e)}"


def handle_dir(folder):
    try:
        if not os.path.isdir(folder):
            return "folder does not exist"

        files = os.listdir(folder)

        if len(files) == 0:
            return "folder is empty"

        return "\n".join(files)

    except Exception as e:
        return f"failed to read folder: {str(e)}"


def handle_delete(file_path):
    try:
        if not os.path.isfile(file_path):
            return "file does not exist"

        os.remove(file_path)

        return "file deleted successfully"

    except Exception as e:
        return f"delete failed: {str(e)}"


def handle_copy_file(source, destination):
    try:
        if not os.path.isfile(source):
            return "source file does not exist"

        shutil.copy(source, destination)

        return "file copied successfully"

    except Exception as e:
        return f"copy failed: {str(e)}"


os.makedirs(BASE_FOLDER, exist_ok=True)

server_socket = socket.socket()

server_socket.bind((HOST, PORT))
server_socket.listen(3)

print(f"server running on port {PORT}")
print(f"server files folder: {BASE_FOLDER}")


while True:
    client_socket, addr = server_socket.accept()

    print(f"{addr[0]} connected")

    while True:
        try:
            command_data = recv_message(client_socket)

            command = command_data.decode()

            print(f"command: {command}")

            if command == "SCREEN":
                handle_screen(client_socket)

            elif command.startswith("COPY "):
                text = command[5:]

                response = handle_copy(text)

                send_message(
                    client_socket,
                    response
                )

            elif command == "PASTE":
                response = handle_paste()

                send_message(
                    client_socket,
                    response
                )

            elif command.startswith("RUN "):
                program = command[4:]

                response = handle_run(program)

                send_message(
                    client_socket,
                    response
                )

            elif command.startswith("DIR "):
                folder = command[4:]

                response = handle_dir(folder)

                send_message(
                    client_socket,
                    response
                )

            elif command.startswith("DELETE "):
                file_name = command[7:]

                response = handle_delete(file_name)

                send_message(
                    client_socket,
                    response
                )

            elif command.startswith("COPYFILE "):
                data = command[9:]

                if "|" not in data:
                    send_message(
                        client_socket,
                        "invalid COPYFILE command"
                    )
                    continue

                source, destination = data.split("|", 1)

                response = handle_copy_file(
                    source,
                    destination
                )

                send_message(
                    client_socket,
                    response
                )

            elif command == "EXIT":
                print(f"{addr[0]} requested disconnect")
                break

            else:
                send_message(
                    client_socket,
                    "unknown command"
                )

        except Exception as e:
            print(
                f"client error: {str(e)}"
            )
            break

    client_socket.close()

    print(f"{addr[0]} disconnected")