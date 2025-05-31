# sensors/sensor.py
import random

class Sensor:
    """
    Klasa bazowa dla symulowanych czujników.
    """
    def __init__(self, sensor_id, name, unit, min_value, max_value, frequency=1):
        self.sensor_id = sensor_id
        self.name = name
        self.unit = unit
        self.min_value = min_value
        self.max_value = max_value
        self.frequency = frequency
        self.active = True
        self.last_value = None

    def read_value(self):
        if not self.active:
            raise RuntimeError(f"Czujnik {self.name} jest wyłączony.")
        value = random.uniform(self.min_value, self.max_value)
        self.last_value = value
        return value

    def calibrate(self, factor):
        if self.last_value is None:
            self.read_value()
        self.last_value *= factor
        return self.last_value

    def get_last_value(self):
        return self.last_value if self.last_value is not None else self.read_value()

    def start(self):
        self.active = True

    def stop(self):
        self.active = False

    def __str__(self):
        return f"Sensor(id={self.sensor_id}, name={self.name}, unit={self.unit})"