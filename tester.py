#!//usr/bin/env python3
import socket
import argparse

target_host = None
target_port = None
timeout = None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def header(msg):
        print(Colors.HEADER + msg + Colors.ENDC)

    @staticmethod
    def fail(msg):
        print(Colors.FAIL + msg + Colors.ENDC)

    @staticmethod
    def testok(msg):
        print(Colors.OKGREEN + msg + Colors.ENDC)

    @staticmethod
    def stepok(msg):
        print(Colors.OKBLUE + msg + Colors.ENDC)

    @staticmethod
    def info(msg):
        print(msg)


def test_00():
    try:
        Colors.header("[Test 00] Connection to the server")
        Colors.info("[Test 00] Awaiting code 220")
        res = str(client.recv(4096))
        if "220" not in res:
            Colors.fail("[Test 00] Wrong response code, expected 220, received: '" + res + "'")
            Colors.fail("[Test 00] Unable to continue testing, exiting...")
            exit(1)
        Colors.stepok("[Test 00] Init OK")
        Colors.info("[Test 00] Sending username")
        client.send(bytes("USER Anonymous\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "331" not in res:
            Colors.fail("[Test 00] Wrong response code, expected 331, received: '" + res + "'")
            Colors.fail("[Test 00] Unable to continue testing, exiting...")
            exit(1)
        Colors.stepok("[Test 00] User OK")
        Colors.info("[Test 00] Sending password")
        client.send(bytes("PASS\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "230" not in res:
            Colors.fail("[Test 00] Wrong response code, expected 230, received: '" + res + "'")
            Colors.fail("[Test 00] Unable to continue testing, exiting...")
            exit(1)
        Colors.stepok("[Test 00] Pass OK")
        Colors.testok("[Test 00] OK")
    except socket.timeout:
        Colors.fail("[Test 00] Connection Timeout: " + str(timeout) + "s")
        Colors.fail("[Test 00] Unable to connect to the server, exiting...")
        exit(1)


def test_01():
    try:
        Colors.header("[Test 01] PASV LIST Command")
        Colors.info("[Test 01] Sending PASV")
        client.send(bytes("PASV\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "227" not in res:
            Colors.fail("[Test 01] Wrong response code, expected 227, received: '" + res + "'")
            Colors.fail("[Test 01] KO")
            return
        data = res.split("(")[1].split(")")[0].split(",")
        data_host = ".".join(data[:4])
        data_port = int(data[4]) * 256 + int(data[5])
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Colors.info("[Test 01] Trying to connect to " + data_host + " on port " + str(data_port))
        data_sock.connect((data_host, data_port))
        data_sock.settimeout(timeout)
        Colors.stepok("[Test 01] Connected")
        Colors.info("[Test 01] Sending LIST")
        client.send(bytes("LIST\r\n", "UTF-8"))
        res = data_sock.recv(4096)
        if len(res) == 0:
            Colors.fail("[Test 01] Empty list response")
            Colors.fail("[Test 01] KO")
            return
        Colors.testok("[Test 01] LIST OK")

    except socket.timeout:
        Colors.fail("[Test 01] Connection Timeout: " + str(timeout) + "s")
        Colors.fail("[Test 01] KO")


def get_args():
    global target_port, target_host, timeout
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    parser.add_argument("--timeout")
    args = parser.parse_args()
    target_host = args.host
    target_port = int(args.port)
    if args.timeout is not None:
        timeout = float(args.timeout)
    else:
        timeout = 5.
    if target_port is None or target_host is None:
        print("invalid host or port")
        exit(1)


if __name__ == "__main__":
    get_args()
    client.connect((target_host, target_port))
    client.settimeout(timeout)
    test_00()
    test_01()
