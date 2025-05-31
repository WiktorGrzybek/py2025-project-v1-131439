# tests/test_sensors.py
import pytest
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor    import HumiditySensor
from sensors.pressure_sensor    import PressureSensor
from sensors.light_sensor       import LightSensor
from sensors.air_quality_sensor import AirQualitySensor

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

def test_light_sensor():
    s = LightSensor('l')
    v1 = s.read_value()
    assert s.min_value <= v1 <= s.max_value

    v2 = s.read_value()
    assert s.min_value <= v2 <= s.max_value

def test_air_quality_sensor():
    s = AirQualitySensor('a')
    v = s.read_value()
    assert s.min_value <= v <= s.max_value

    high = False
    for _ in range(100):
        v2 = s.read_value()
        if v2 >= 200:
            high = True
            break
    assert s.min_value <= v2 <= s.max_value

