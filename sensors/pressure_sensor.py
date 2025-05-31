# sensors/pressure_sensor.py
import random
from .sensor import Sensor

class PressureSensor(Sensor):
    """
    Symulacja ciśnienia atmosferycznego.
    Zakres: 950 hPa–1050 hPa.
    """
    def __init__(self, sensor_id, name="PressureSensor", unit="hPa",
                 min_value=950.0, max_value=1050.0, frequency=1):
        super().__init__(sensor_id, name, unit, min_value, max_value, frequency)

    def read_value(self):
        if not self.active:
            raise RuntimeError(f"Czujnik {self.name} jest wyłączony.")
        base = random.uniform(self.min_value, self.max_value)
        noise = random.gauss(0, 1)
        value = max(self.min_value, min(self.max_value, base + noise))
        self.last_value = value
        return value
