import socket


class Client:
    def __init__(self, host, port, timeout, verbose):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.client.settimeout(timeout)
        self.verbose = verbose

    def __del__(self):
        self.client.close()

    def recv(self):
        return self.client.recv(4096).decode("utf-8")

    def send(self, msg):
        print(f'[Client] Sending "{msg}"')
        self.client.send(bytes(msg + "\r\n", "utf-8"))