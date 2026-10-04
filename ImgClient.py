import socket
import os


SERVER_IP = "127.0.0.1"
PORT = 1450


def send_file(sock, file_path):
    """
    Sends an image file to the server.
    """
    file_name = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        file_data = f.read()

    file_name_data = file_name.encode()
    file_name_len = str(len(file_name_data)).zfill(2)
    file_data_len = str(len(file_data)).zfill(6)

    sock.sendall(file_name_len.encode())
    sock.sendall(file_name_data)
    sock.sendall(file_data_len.encode())
    sock.sendall(file_data)


my_soc = socket.socket()

try:
    my_soc.connect((SERVER_IP, PORT))

except Exception as e:
    print(f"{str(e)} - server is down - try again later")
    my_soc.close()
    exit()


while True:
    file_path = input("Enter image file path or q to end: ")

    if file_path.lower() == "q":
        break

    extension = os.path.splitext(file_path)[1].lower()

    if extension not in [".jpg", ".png", ".jpeg", ".bmp"]:
        print("Not a valid image file - try again")
        continue

    if not os.path.isfile(file_path):
        print("Image file does not exist - try again")
        continue

    try:
        send_file(my_soc, file_path)
        print("The image file was successfully sent to the server")

    except Exception as e:
        print(f"{str(e)} - problem sending data - try again later")
        break


my_soc.close()
print("Bye bye")