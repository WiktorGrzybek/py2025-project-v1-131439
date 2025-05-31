# sensors/light_sensor.py
import math
from .sensor import Sensor

class LightSensor(Sensor):
    """
    Czujnik natężenia oświetlenia (LightSensor):

    Parametry: Zakres w luksach – np. 0 lx (noc) do 10000 lx (słoneczny dzień).
    Specyfika: Symulacja zmian oświetlenia w zależności od pory dnia.
    """
    def __init__(self, sensor_id, name="LightSensor", unit="lx",
                 min_value=0.0, max_value=10000.0, frequency=1):
        super().__init__(sensor_id, name, unit, min_value, max_value, frequency)
        self._t = 0

    def read_value(self):
        if not self.active:
            raise RuntimeError(f"Czujnik {self.name} jest wyłączony.")
        day_seconds = 24 * 60 * 60
        theta = 2 * math.pi * (self._t % day_seconds) / day_seconds - math.pi/2
        raw = (math.sin(theta) + 1) / 2  # od 0 do 1
        value = self.min_value + raw * (self.max_value - self.min_value)
        self.last_value = value
        self._t += self.frequency
        return value
