# network/client.py
import socket
import yaml
import json
from threading import Thread

class NetworkClient:
    """
    TCP klient odbierający komunikaty JSON od serwera.
    """
    def __init__(self, config_path="network/config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        cli = cfg['client']
        self.host = cli['server_host']
        self.port = cli['server_port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.running = True
        Thread(target=self._receive_loop, daemon=True).start()

    def _receive_loop(self):
        buffer = ''
        while self.running:
            chunk = self.sock.recv(1024).decode()
            if not chunk:
                break
            buffer += chunk
            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                try:
                    print(json.loads(line))
                except json.JSONDecodeError:
                    print("Invalid JSON received")

    def close(self):
        self.running = False
        self.sock.close()