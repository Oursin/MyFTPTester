from .Logger import Logger
import socket


def test(client, timeout):
    Logger.set_test("02")
    try:
        Logger.test("PASV LIST Command")
        Logger.info("Sending PASV")
        client.send(bytes("PASV\r\n", "UTF-8"))
        res = client.recv(4096).decode("utf-8")
        if "227" not in res:
            Logger.fail(f"Wrong response code, expected 227, received: '{res}'")
            Logger.fail("KO")
            return False
        data = res.split("(")[1].split(")")[0].split(",")
        data_host = ".".join(data[:4])
        data_port = int(data[4]) * 256 + int(data[5])
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Logger.info("Trying to connect to " + data_host + " on port " + str(data_port))
        data_sock.connect((data_host, data_port))
        data_sock.settimeout(timeout)
        Logger.stepok("Connected")
        Logger.info("Sending LIST")
        client.send(bytes("LIST\r\n", "UTF-8"))
        res = data_sock.recv(4096).decode("utf-8")
        if len(res) == 0:
            Logger.fail("Empty list response")
            Logger.fail("KO")
            return False
        if "file" not in res:
            Logger.fail("")
        Logger.stepok("LIST OK")
        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail("Connection Timeout: " + str(timeout) + "s")
        Logger.fail("KO")
        return False
