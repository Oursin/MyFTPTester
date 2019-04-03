from .Logger import Logger
import socket


def test(client, timeout):
    Logger.set_test("03")
    try:
        Logger.header("NOOP")

        client.send("NOOP")
        res = client.recv()
        if "200" not in res:
            Logger.fail(f"Wrong response code, expected 200, received: '{res}'")
            Logger.fail("Unable to continue testing, exiting...")
            exit(1)
        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail("Connection Timeout: " + str(timeout) + "s")
        Logger.fail("Unable to connect to the server, exiting...")
        exit(1)
