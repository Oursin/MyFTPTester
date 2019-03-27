#!//usr/bin/env python3
import socket
import argparse
from os import listdir
from tests.Logger import Logger
import subprocess

target_host = "127.0.0.1"
target_port = 4242
timeout = None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def get_args():
    global target_port, target_host, timeout
    parser = argparse.ArgumentParser()
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
    subprocess.run(["../myftp", "4242", "."])
    get_args()
    client.connect((target_host, target_port))
    client.settimeout(timeout)
    files = [f.split(".")[0] for f in listdir("./tests") if "test" in f]
    files.sort()
    total = 0
    for test in files:
        total += 1 if __import__("tests." + test, fromlist=[""]).test(client, timeout) else 0
    print()
    Logger.res("--- SUMMARY ---")
    Logger.testok(str(total) + " test(s) passed")
    Logger.fail(str(len(files) - total) + " test(s) failed")
