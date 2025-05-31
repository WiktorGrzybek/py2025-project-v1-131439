# sensors/humidity_sensor.py
import random
from .sensor import Sensor

class HumiditySensor(Sensor):
    """
    Symulacja wilgotności z losowym szumem.
    Zakres: 0%–100%.
    """
    def __init__(self, sensor_id, name="HumiditySensor", unit="%RH",
                 min_value=0.0, max_value=100.0, frequency=1):
        super().__init__(sensor_id, name, unit, min_value, max_value, frequency)

    def read_value(self):
        if not self.active:
            raise RuntimeError(f"Czujnik {self.name} jest wyłączony.")
        base = random.uniform(self.min_value, self.max_value)
        noise = random.gauss(0, 2)
        value = max(self.min_value, min(self.max_value, base + noise))
        self.last_value = value
        return value
