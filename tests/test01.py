from .Logger import Logger
import socket


"""

Scenario ideas :

    - Add CWDUP
    - Go back when at the root

"""

def test(client, timeout):
    try:
        Logger.header("[Test 01] CWD/PWD")

        Logger.info("[Test 01] Sending PWD")
        client.send(bytes("PWD\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if '257 "/"' not in res:
            if "257" not in res:
                Logger.fail("[Test 01] Wrong response code, expected 257, received: '" + res + "'")
            else:
                Logger.fail("[Test 01] Wrong base path, should be \"/\", received: '" + res + "'")
            Logger.fail("[Test 01] KO")
            return False
        Logger.stepok("[Test 01] Base PWD OK")

        Logger.info("[Test 01] Sending CWD public")
        client.send(bytes("CWD public\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "250" not in res:
            Logger.fail("[Test 01] Wrong response code, expected 250, received: '" + res + "'")
            Logger.fail("[Test 01] KO")
            return False
        Logger.stepok("[Test 01] CWD OK")

        Logger.info("[Test 01] Sending PWD")
        client.send(bytes("PWD\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if '257 "/public' not in res:
            if "257" not in res:
                Logger.fail("[Test 01] Wrong response code, expected 257, received: '" + res + "'")
            else:
                Logger.fail("[Test 01] Wrong base path, should be \"/\", received: '" + res + "'")
            Logger.fail("[Test 01] KO")
            return False
        Logger.stepok("[Test 01] PWD OK")
        Logger.testok("[Test 01] OK")
        return True
    except socket.timeout:
        Logger.fail("[Test 01] Connection Timeout: " + str(timeout) + "s")
        Logger.fail("[Test 01] Unable to connect to the server, exiting...")
        return False
