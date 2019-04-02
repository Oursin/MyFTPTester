from .Logger import Logger
import socket
import os


"""

Scenario ideas :

    - Add CDUP
    - Go back when at the root

"""


def test(client, timeout):
    Logger.set_test("01")
    try:
        Logger.header("CWD/PWD")

        Logger.info("Sending PWD")
        client.send(bytes("PWD\r\n", "UTF-8"))
        res = client.recv(4096).decode("utf-8")
        cwd = os.getcwd()
        if f'257 "{cwd}"' not in res:
            if "257" not in res:
                Logger.fail(f"Wrong response code, expected 257, received: '{res}'")
            else:
                Logger.fail(f"Wrong base path, should be \"/\", received: '{res}'")
            Logger.fail("KO")
            return False
        Logger.stepok("Base PWD OK")

        Logger.info("Sending CWD public")
        client.send(bytes("CWD public\r\n", "UTF-8"))
        res = client.recv(4096).decode("utf-8")
        if "250" not in res:
            Logger.fail(f"Wrong response code, expected 250, received: '{res}'")
            Logger.fail("KO")
            return False
        Logger.stepok("CWD OK")

        Logger.info("Sending PWD")
        client.send(bytes("PWD\r\n", "UTF-8"))
        res = client.recv(4096).decode("utf-8")
        if f'257 {cwd}/public' not in res:
            if "257" not in res:
                Logger.fail(f"Wrong response code, expected 257, received: '{res}'")
            else:
                Logger.fail(f"Wrong base path, should be \"/\", received: '{res}'")
            Logger.fail("KO")
            return False
        Logger.stepok("PWD OK")
        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail(f"Connection Timeout: {str(timeout)}s")
        Logger.fail("Unable to connect to the server, exiting...")
        return False
