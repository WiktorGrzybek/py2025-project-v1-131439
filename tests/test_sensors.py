# tests/test_sensors.py
import pytest
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor
from sensors.pressure_sensor import PressureSensor


def test_temperature():
    s = TemperatureSensor('t')
    v = s.read_value()
    assert s.min_value <= v <= s.max_value


def test_humidity():
    s = HumiditySensor('h')
    v = s.read_value()
    assert s.min_value <= v <= s.max_value


def test_pressure():
    s = PressureSensor('p')
    v = s.read_value()
    assert s.min_value <= v <= s.max_value