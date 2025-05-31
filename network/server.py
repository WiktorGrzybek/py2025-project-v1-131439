# network/server.py
import socket
import threading
import yaml
import json
from datetime import datetime

from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor    import HumiditySensor
from sensors.pressure_sensor    import PressureSensor
from sensors.light_sensor       import LightSensor
from sensors.air_quality_sensor import AirQualitySensor

class NetworkServer:
    """
    TCP serwer przesyłający odczyty czujników w formacie JSON.
    """
    def __init__(self, config_path="network/config.yaml"):
        with open(config_path) as f:
            cfg = yaml.safe_load(f)
        srv = cfg['server']
        self.host = srv['host']
        self.port = srv['port']
        self.sensors = [
            TemperatureSensor('temp1'),
            HumiditySensor('hum1'),
            PressureSensor('pres1'),
            LightSensor('light1'),
            AirQualitySensor('airq1')
        ]
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"Listening on {self.host}:{self.port}")
        while True:
            client, _ = self.sock.accept()
            threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()

    def _handle_client(self, client):
        try:
            for s in self.sensors:
                data = {
                    'sensor':   s.sensor_id,
                    'value':    s.read_value(),
                    'unit':     s.unit,
                    'timestamp': datetime.now().isoformat()
                }
                client.send((json.dumps(data) + '\n').encode())
        except Exception as e:
            print(f"Client error: {e}")
        finally:
            client.close()
