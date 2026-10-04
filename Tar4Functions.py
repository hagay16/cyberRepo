import os
import shutil
import subprocess
import pyperclip
import platform
from PIL import ImageGrab

SYSTEMNAME = platform.system()


if SYSTEMNAME == "Windows":
    ALLOWED_PROGRAMS = {        #i do this so the program can work on my linux pc too,
        "calc": "calc.exe",     #because the program names are different
        "google": "chrome.exe"
    }
else:
    ALLOWED_PROGRAMS = {
        "calc": "gnome-calculator",
        "google": "google-chrome"
    }



def send_screen(sock):
    """
    Takes a screenshot of the server and sends it to the client.

    on windows it uses ImageGrab
    on linux it uses gnome-screenshot.

    :param sock: client socket
    :return: None
    """
    if SYSTEMNAME == "Windows":
        im = ImageGrab.grab()
        im.save("screen.jpg")
    elif SYSTEMNAME == "Linux":
        subprocess.run(["gnome-screenshot", "-f", "screen.jpg"])

    with open("screen.jpg", "rb") as file:
        image_data = file.read()

    image_len = str(len(image_data)).zfill(7)

    sock.sendall(image_len.encode())
    sock.sendall(image_data)


def recv_big_data(sock, data_len):
    """
    Receives data in chunks of up to 1024 bytes.
    return: received bytes
    """
    data = b""

    while len(data) < data_len:
        amount_left = data_len - len(data)

        if amount_left > 1024:
            chunk = sock.recv(1024)
        else:
            chunk = sock.recv(amount_left)

        if chunk == b"":
            raise ConnectionError("client disconnected")

        data += chunk

    return data


def copy_to_clipboard(text):
    """
    Copies text to the server clipboard
    return: True if the operation succeeded
    """
    pyperclip.copy(text)
    return pyperclip.paste() == text


def paste_from_clipboard():
    """
    Reads text from the server clipboard.
    return: clipboard text
    """
    return pyperclip.paste()


def run_program(program):
    """
    Runs an allowed program on the server.
    return: result message
    """
    program = program.lower()

    if program not in ALLOWED_PROGRAMS:
        return "program is not allowed"

    try:
        subprocess.Popen([ALLOWED_PROGRAMS[program]])
        return "program started successfully"
    except Exception:
        return "program failed to start"


def get_folder_content(folder):
    """
    Returns the content of a folder.

    :param folder: folder path
    :return: folder content as a string
    """
    files = os.listdir(folder)
    return "\n".join(files)


def delete_file(file_path):
    """
    Deletes a file.

    :param file_path: path of the file to delete
    :return: True if the file was deleted
    """
    if not os.path.isfile(file_path):
        return False

    os.remove(file_path)
    return True


def copy_file(source, destination):
    """
    Copies a file.

    :param source: source file path
    :param destination: destination file path
    :return: True if the file was copied
    """
    if not os.path.isfile(source):
        return False

    shutil.copy(source, destination)
    return True