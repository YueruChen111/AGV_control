# manual send cocomm message
import socket, os

if os.path.exists("/tmp/CO_command_socket"):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect("/tmp/CO_command_socket")
    while True:
        x = "[1] " + input("> ") + "\r\n"
        if "" != x:
            print("SEND:", x.encode("utf-8"))
            client.send(x.encode("utf-8"))
            print("RECEIVE:", client.recv(1024))
    client.close()
else:
    print("Couldn't Connect!")