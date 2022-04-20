import socket
import select
import errno
import sys

HEADER_LENGTH = 10


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# here we asking for the target website
# or host
target_ip = socket.gethostname()
print('Starting scan on host:', target_ip)

# function for scanning ports


def port_scan(port):
    try:
        s.connect((target_ip, port))
        return True
    except:
        return False

PORT =9971
for port in range(9960, 9971):
    if not port_scan(port):
        print(f'port {port} is closed')
    else:
        print(f'port {port} is open')
        PORT = port
IP = socket.gethostname()
s.close()

if PORT%2==0:
    print("Connected to a multi user message server!")
    my_username = input("Username:  ")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, PORT))
    client_socket.setblocking(False)

    username = my_username.encode('utf-8')
    username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(username_header+username)

    while True:
        
        message = input(f"{my_username}>>>> ")
        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):>{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header+message)
        try:
            while True:
                # recieve Things
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username):
                    print("connection closed by the server")
                    sys.exit()
                username_length = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_length).decode('utf-8')

                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                print(f"{username}>>>> {message}")

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Reading error', str(e))
                sys.exit()
            continue

        except Exception as e:
            print("General error: ", str(e))
            sys.exit()
else:
    
    print("Connected to a voting server!")
    
    my_username=input("Username: ")

    client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((IP,PORT))
    client_socket.setblocking(False)

    username=my_username.encode("utf-8")
    username_header=f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(username_header+username)


    while True:
        message=input(f"{my_username} > ")
        if message:
            message=message.encode("utf-8")
            message_header=f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header+message)
        
        try:
            while True:
                username_header=client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Connection Closed by the server");
                    sys.exit()

                username_length=int(username_header.decode("utf-8").strip())
                username=client_socket.recv(username_length).decode("utf-8")

                message_header=client_socket.recv(HEADER_LENGTH)
                message_length=int(message_header.decode("utf-8").strip())
                message=client_socket.recv(message_length).decode("utf-8")

                print(f"{username} > {message}")
                print("THANKYOU FOR YOUR VOTE:")
                sys.exit()

        except IOError as e:
            if e.errno !=errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("THANKYOU FOR YOUR VOTE:")
                sys.exit()
            continue
        except Exception as e:
            print("General Error: ",str(e))
            sys.exit()        
