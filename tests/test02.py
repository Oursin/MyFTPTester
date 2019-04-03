from .Logger import Logger
from .Client import Client
import socket


def create_pasv(client, timeout, verbose):
    client.send("PASV")
    res = client.recv()
    if "227" not in res:
        Logger.fail(f"Wrong response code, expected 227, received: '{res}'")
        Logger.fail("KO")
        return None
    data = res.split("(")[1].split(")")[0].split(",")
    data_host = ".".join(data[:4])
    data_port = int(data[4]) * 256 + int(data[5])

    Logger.info("Trying to connect to " + data_host + " on port " + str(data_port))
    data_conn = Client(data_host, data_port, timeout, verbose)
    Logger.stepok("Connected")
    return data_conn


def check_list(client, data, arg, search):
    client.send(f"LIST {arg}")
    res = data.recv()
    if len(res) == 0:
        Logger.fail("Empty list response")
        Logger.fail("KO")
        return False
    if search not in res:
        Logger.fail(f"No directory named public found, received {res}")
        Logger.fail("KO")
        return False
    res = client.recv()
    if "150" not in res:
        Logger.fail(
            f"Wrong response code, expected 150 (the server should send a message before listing), received: '{res}'\n")
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
        Logger.header("PASV LIST Command")

        data = create_pasv(client, timeout, verbose)
        if data is None:
            return False
        if not check_list(client, data, "", "public"):
            return False
        Logger.stepok("LIST Basic OK")

        data = create_pasv(client, timeout)
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
