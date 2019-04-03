from .Logger import Logger
import socket
import os


def check_cwd(client, target):
    client.send(f"CWD {target}")
    res = client.recv()
    if "250" not in res:
        Logger.fail(f"Wrong response code, expected 250, received: '{res}'")
        Logger.fail("KO")
        return False
    return True


def check_cdup(client, target):
    client.send(f"CDUP")
    res = client.recv()
    if "250" not in res:
        Logger.fail(f"Wrong response code, expected 250, received: '{res}'")
        Logger.fail("KO")
        return False
    return True


def check_pwd(client, target):
    client.send("PWD")
    res = client.recv()
    if f'257 "{target}"' not in res:
        if "257" not in res:
            Logger.fail(f"Wrong response code, expected 257, received: '{res}'")
        else:
            Logger.fail(f"Wrong base path, should be {target}, received: '{res}'")
        Logger.fail("KO")
        return False
    return True


def test(client, timeout, _):
    Logger.set_test("01")
    cwd = os.getcwd()
    try:
        Logger.header("CWD/PWD")

        if not check_pwd(client, cwd):
            return False
        Logger.stepok("Base PWD OK")

        if not check_cwd(client, "public"):
            return False
        Logger.stepok("CWD OK")

        if not check_pwd(client, f"{cwd}/public"):
            return False
        Logger.stepok("PWD OK")

        Logger.info("Root of the system")
        if not check_cwd(client, "/"):
            return False
        if not check_cwd(client, ".."):
            return False
        if not check_pwd(client, "/"):
            return False
        Logger.stepok("Root OK")

        Logger.info("[BONUS] CDUP")
        if not check_cwd(client, f"{cwd}/public"):
            return False
        if check_cdup(client, cwd):
            Logger.stepok("[BONUS] CDUP OK")

        Logger.testok("OK")
        return True
    except socket.timeout:
        Logger.fail(f"Connection Timeout: {str(timeout)}s")
        Logger.fail("Unable to connect to the server, exiting...")
        return False
