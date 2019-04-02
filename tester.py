#!//usr/bin/env python3
import socket
import argparse
from os import listdir, getcwd
from tests.Logger import Logger
from tests.Client import Client
import subprocess

timeout = None


def get_args():
    global timeout
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout")
    args = parser.parse_args()
    if args.timeout is not None:
        timeout = float(args.timeout)
    else:
        timeout = 5.


if __name__ == "__main__":
    proc = subprocess.Popen(["../myftp", "4242", getcwd()])
    get_args()
    client = Client("127.0.0.1", 4242, timeout)
    files = [f.split(".")[0] for f in listdir("./tests") if "test" in f]
    files.sort()
    total = 0
    for test in files:
        total += 1 if __import__("tests." + test, fromlist=[""]).test(client, timeout) else 0
    print()
    Logger.set_test("")
    Logger.res("--- SUMMARY ---")
    Logger.testok(str(total) + " test(s) passed")
    Logger.fail(str(len(files) - total) + " test(s) failed")
    proc.kill()
