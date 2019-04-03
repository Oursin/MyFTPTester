from .Logger import Logger
from .Passive import passive
import socket


def check_list(client, data, arg, search):
    client.send(f"LIST {arg}")

    res = client.recv()
    if "150" not in res:
        Logger.fail(
            f"Wrong response code, expected 150 (the server should send a message before listing), received: '{res}'\n")
        Logger.fail("KO")
        return False
    res = data.recv()
    if len(res) == 0:
        Logger.fail("Empty list response")
        Logger.fail("KO")
        return False
    if search not in res:
        Logger.fail(f"No directory named {search} found, received {res}")
        Logger.fail("KO")
        return False

    res = client.recv()
    if "226" not in res:
        Logger.fail(
            f"Wrong response code, expected 150 (the server should send a message after listing), received: '{res}'\n")
        Logger.fail("KO")
        return False

    return True


def test(client, timeout, verbose):
    Logger.set_test("02")
    try:
        Logger.header("Passive LIST")

        data = passive(client, timeout, verbose)
        if data is None:
            return False
        if not check_list(client, data, "", "public"):
            return False
        Logger.stepok("LIST Basic OK")

        data = passive(client, timeout, verbose)
        if data is None:
            return False
        if not check_list(client, data, "public", "file"):
            return False

        Logger.stepok("LIST argument OK")
        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail("Connection Timeout: " + str(timeout) + "s")
        Logger.fail("KO")
        return False
