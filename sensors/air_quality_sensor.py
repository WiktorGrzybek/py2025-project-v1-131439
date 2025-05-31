# sensors/air_quality_sensor.py
import random
from .sensor import Sensor

class AirQualitySensor(Sensor):
    """
    Czujnik jakości powietrza (AirQualitySensor):

    Parametry: Poziom zanieczyszczeń, np. indeks AQI od 0 do 500.
    Specyfika: Generowanie wartości, które mogą wskazywać zarówno dobre, jak i złe
              warunki środowiskowe, możliwość symulacji nagłych spadków lub wzrostów.
    """
    def __init__(self, sensor_id, name="AirQualitySensor", unit="AQI",
                 min_value=0.0, max_value=500.0, frequency=1):
        super().__init__(sensor_id, name, unit, min_value, max_value, frequency)
        self._current = random.uniform(20, 80)

    def read_value(self):
        if not self.active:
            raise RuntimeError(f"Czujnik {self.name} jest wyłączony.")
        base = self._current
        if random.random() < 0.05:
            value = random.uniform(200, self.max_value)
        else:
            noise = random.gauss(0, 10)
            value = max(self.min_value, min(self.max_value, base + noise))
        self.last_value = value
        self._current = value
        return value
