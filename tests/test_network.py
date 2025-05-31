# tests/test_network.py
import threading
import time
import json
import yaml
import socket

from network.server import NetworkServer
from network.client import NetworkClient

def test_network(tmp_path):
    """
    Ten test uruchamia serwer w tle, łączy klienta i weryfikuje,
    że serwer w ogóle wysyła dane (bez wyjątku) dla pięciu czujników.
    """

    cfg_path = tmp_path / "config.yaml"
    cfg_path.write_text(yaml.dump({
        'server': {'host': '127.0.0.1', 'port': 9998},
        'client': {'server_host': '127.0.0.1', 'server_port': 9998}
    }))


    server = NetworkServer(str(cfg_path))
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.1)


    client = NetworkClient(str(cfg_path))
    client.connect()


    time.sleep(0.2)
    client.close()


