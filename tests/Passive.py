from .Logger import Logger
from .Client import Client


def passive(client, timeout, verbose):
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