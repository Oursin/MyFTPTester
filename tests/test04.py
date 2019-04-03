from .Logger import Logger
from .Passive import passive
import socket


def check_recv(client, data, target, content):
    client.send(f"RETR {target}")

    res = client.recv()
    if "150" not in res:
        Logger.fail(
            f"Wrong response code, expected 150 (the server should send a message before sending the file), received: '{res}'\n")
        Logger.fail("KO")
        return False

    res = data.recv
    if content not in res:
        Logger.fail(f"{content} not found in file, received {res}")
        Logger.fail("KO")
        return False

    res = client.recv()
    if "226" not in res:
        Logger.fail(f"Wrong response code, expected 226, was {res}")
        Logger.fail("KO")
        return False

    return True


def test(client, timeout, v):
    Logger.set_test("03")
    try:
        Logger.header("Passive RETR")

        data = passive(client, timeout, v)
        if data is None:
            return False
        if not check_recv(client, data, "public/file", "OK"):
            return False

        Logger.stepok("Basic RETR OK")
        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail("Connection Timeout: " + str(timeout) + "s")
        Logger.fail("Unable to connect to the server, exiting...")
        exit(1)
