from .Logger import Logger
import socket


def test(client, timeout):
    try:
        Logger.header("[Test 02] PASV LIST Command")
        Logger.info("[Test 02] Sending PASV")
        client.send(bytes("PASV\r\n", "UTF-8"))
        res = str(client.recv(4096))
        if "227" not in res:
            Logger.fail("[Test 02] Wrong response code, expected 227, received: '" + res + "'")
            Logger.fail("[Test 02] KO")
            return False
        data = res.split("(")[1].split(")")[0].split(",")
        data_host = ".".join(data[:4])
        data_port = int(data[4]) * 256 + int(data[5])
        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Logger.info("[Test 02] Trying to connect to " + data_host + " on port " + str(data_port))
        data_sock.connect((data_host, data_port))
        data_sock.settimeout(timeout)
        Logger.stepok("[Test 02] Connected")
        Logger.info("[Test 02] Sending LIST")
        client.send(bytes("LIST\r\n", "UTF-8"))
        res = data_sock.recv(4096)
        if len(res) == 0:
            Logger.fail("[Test 02] Empty list response")
            Logger.fail("[Test 02] KO")
            return False
        Logger.stepok("[Test 02] LIST OK")
        Logger.testok("[Test 02] OK")
        return True
    except socket.timeout:
        Logger.fail("[Test 02] Connection Timeout: " + str(timeout) + "s")
        Logger.fail("[Test 02] KO")
        return False
