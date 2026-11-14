import socket


def recv_response(sock):
    """
    Receive a response from the server.
    first receives 4 bytes of the response length,
    then receives the response itself.
    return: response from server
    """
    length = int(sock.recv(4).decode())
    data = sock.recv(length).decode()

    return data

def is_valid_ip(ip):
    parts = ip.split(".")
    res = True
    if len(parts) != 4:  # Must have exactly 4 parts
        res = False
    else:
        for part in parts:
            # Check if the part is purely digits (rejects empty strings, spaces, or negatives)
            if not part.isdigit():
                res = False
            else:
                # Reject leading zeros (e.g., "01" is invalid, "0" is valid)
                if len(part) > 1 and part.startswith("0"):
                    res = False
                else:
                    num = int(part) # Convert to integer and check range 0-255
                    if num < 0 or num > 255:
                        res = False

    return res

def check_next(choice,object):
    my_sock = socket.socket()

    try:
        my_sock.connect(("127.0.0.1", 1450))
    except Exception as e:
        my_sock.close()
        exit(f"server is down - try again later: {str(e)}")
    my_sock.send(str(len(choice)).zfill(8).encode())
    my_sock.send(choice.encode())
    my_sock.send(str(len(object)).zfill(10).encode())
    my_sock.send(object.encode())

    try:
        response = recv_response(my_sock)
    except Exception as e:
        print(f"error receiving data: {str(e)}")

    my_sock.close()
    return response




IP_to_HostName = {"1.1.1.1":"OnePointOne","1.2.3.4":"myWebsite"}
HostName_to_IP = {"OnePointOne":"1.1.1.1","myWebsite":"1.2.3.4"}


while True:
    choice = input("Choose ip, host name or exit: ").lower().replace(" ", "")

    if choice == "exit":
        break

    elif choice == "ip":
        ip = input("enter ip address: ")
        if not is_valid_ip(ip):
            print("invalid ip address")
        elif ip in IP_to_HostName:
            print(f"your host name for ip: {ip}, is: {IP_to_HostName[ip]}")
        else:
            print("ip was not found in local dns, looking in regional dns...")
            # here look in regional dns
            response = check_next(choice,ip)
            print(f"your host name for ip: {ip}, is: {response}")
            IP_to_HostName[ip] = response

    elif choice == "hostname":
        hostName = input("enter host name: ")

        if hostName in HostName_to_IP:
            print(f"your ip for host name: {hostName}, is: {HostName_to_IP[hostName]}")
        else:
            print("host name was not found in local dns, looking in regional dns...")
            # here look in regional dns
            response = check_next(choice, hostName)
            print(f"your ip for host name: {hostName}, is: {response}")
            HostName_to_IP[hostName] = response
    else:
        print("Enter a valid choice (ip or host name)")