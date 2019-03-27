from .Logger import Logger
import socket


def test(client, timeout):
    try:
        Logger.header("[Test 00] Connection to the server")
        Logger.info("[Test 00] Awaiting code 220")
        res = str(client.recv(4096))
        if "220" not in res:
            Logger.fail("[Test 00] Wrong response code, expected 220, received: '" + res + "'")
            Logger.fail("[Test 00] Unable to continue testing, exiting...")
            exit(1)
        Logger.stepok("[Test 00] Init OK")
        Logger.info("[Test 00] Sending username")
        client.send(bytes("USER Anonymous\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "331" not in res:
            Logger.fail("[Test 00] Wrong response code, expected 331, received: '" + res + "'")
            Logger.fail("[Test 00] Unable to continue testing, exiting...")
            exit(1)
        Logger.stepok("[Test 00] User OK")
        Logger.info("[Test 00] Sending password")
        client.send(bytes("PASS\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "230" not in res:
            Logger.fail("[Test 00] Wrong response code, expected 230, received: '" + res + "'")
            Logger.fail("[Test 00] Unable to continue testing, exiting...")
            exit(1)
        Logger.stepok("[Test 00] Pass OK")
        Logger.testok("[Test 00] OK")
    except socket.timeout:
        Logger.fail("[Test 00] Connection Timeout: " + str(timeout) + "s")
        Logger.fail("[Test 00] Unable to connect to the server, exiting...")
        exit(1)