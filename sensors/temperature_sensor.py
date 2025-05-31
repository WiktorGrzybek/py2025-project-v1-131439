# sensors/temperature_sensor.py
import math
from .sensor import Sensor

class TemperatureSensor(Sensor):
    """
    Symulacja cyklu dobowego temperatury (sinusoidalnie).
    Zakres: -20°C–50°C.
    """
    def __init__(self, sensor_id, name="TemperatureSensor", unit="°C",
                 min_value=-20.0, max_value=50.0, frequency=1):
        super().__init__(sensor_id, name, unit, min_value, max_value, frequency)
        self._time = 0

    def read_value(self):
        if not self.active:
            raise RuntimeError(f"Czujnik {self.name} jest wyłączony.")
        midpoint = (self.max_value + self.min_value) / 2
        amplitude = (self.max_value - self.min_value) / 2
        value = midpoint + amplitude * math.sin(self._time / 60)
        self._time += self.frequency
        self.last_value = value
        return value
