#!//usr/bin/env python3
import socket
import argparse
from os import listdir

target_host = None
target_port = None
timeout = None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


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
    files = [f.split(".")[0] for f in listdir("./tests") if "test" in f]
    files.sort()
    for test in files:
        __import__("tests." + test, fromlist=[""]).test(client, timeout)
