from .Logger import Logger
import socket


def test(client, timeout):
    Logger.set_test("00")
    try:
        Logger.test("Connection to the server")
        Logger.info("Awaiting code 220")
        res = client.recv(4096).decode("utf-8")
        if "220" not in res:
            Logger.fail(f"Wrong response code, expected 220, received: '{res}'")
            Logger.fail("Unable to continue testing, exiting...")
            exit(1)
        Logger.stepok("Init OK")
        Logger.info("Sending username")
        client.send(bytes("USER Anonymous\r\n", "UTF-8"))
        res = client.recv(4096).decode("utf-8")
        if "331" not in res:
            Logger.fail(f"Wrong response code, expected 331, received: '{res}'")
            Logger.fail("Unable to continue testing, exiting...")
            exit(1)
        Logger.stepok("User OK")
        Logger.info("Sending password")
        client.send(bytes("PASS\r\n", "UTF-8"))
        res = client.recv(4096).decode("utf-8")
        if "230" not in res:
            Logger.fail(f"Wrong response code, expected 230, received: '{res}'")
            Logger.fail("Unable to continue testing, exiting...")
            exit(1)
        Logger.stepok("Pass OK")
        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail("Connection Timeout: " + str(timeout) + "s")
        Logger.fail("Unable to connect to the server, exiting...")
        exit(1)
