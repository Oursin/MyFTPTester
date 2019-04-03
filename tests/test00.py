from .Logger import Logger
import socket


def test(client, timeout, _):
    Logger.set_test("00")
    try:
        Logger.header("Connection to the server")
        Logger.info("Awaiting code 220")

        res = client.recv()
        if "220" not in res:
            Logger.fail(f"Wrong response code, expected 220, received: '{res}'")
            Logger.fail("Unable to continue testing, exiting...")
            exit(1)

        Logger.stepok("Init OK")
        Logger.info("Sending username")

        client.send("USER Anonymous")
        res = client.recv()
        if "331" not in res:
            Logger.fail(f"Wrong response code, expected 331, received: '{res}'")
            Logger.fail("Unable to continue testing, exiting...")
            exit(1)

        Logger.stepok("User OK")
        Logger.info("Sending password")

        client.send("PASS")
        res = client.recv()
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
