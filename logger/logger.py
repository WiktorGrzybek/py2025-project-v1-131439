# logger/logger.py
import os
import csv
import json
from datetime import datetime

class Logger:
    """
    Logger zapisujący odczyty czujników do plików CSV
    z automatyczną rotacją i retencją.
    """
    def __init__(self, config_path="logger/config.json"):
        base = os.path.dirname(__file__)
        full_path = os.path.join(base, os.path.basename(config_path))
        with open(full_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)

        self.log_dir   = cfg["log_dir"]
        self.pattern   = cfg["filename_pattern"]
        self.max_size  = cfg["max_size_mb"]
        self.retention = cfg["backup_count"]
        self.buffer_size = cfg["buffer_size"]
        self._buffer = []

        os.makedirs(self.log_dir, exist_ok=True)
        self._open_file()

    def _open_file(self):
        if hasattr(self, 'file'):
            self.file.close()
        name = datetime.now().strftime(self.pattern)
        self.current = os.path.join(self.log_dir, name)
        new = not os.path.exists(self.current)
        self.file = open(self.current, 'a', newline='')
        self.writer = csv.writer(self.file)
        if new:
            self.writer.writerow(["timestamp", "sensor_id", "value", "unit"])

    def log_reading(self, sensor_id, timestamp, value, unit):
        self._buffer.append([timestamp.isoformat(), sensor_id, value, unit])
        if len(self._buffer) >= self.buffer_size:
            self._flush()
        self._rotate_if_needed()

    def _flush(self):
        for row in self._buffer:
            self.writer.writerow(row)
        self.file.flush()
        self._buffer.clear()

    def _rotate_if_needed(self):
        size_mb = os.path.getsize(self.current) / (1024 * 1024)
        if size_mb >= self.max_size:
            self._rotate()

    def _rotate(self):
        self.file.close()
        for i in range(self.retention - 1, 0, -1):
            src = f"{self.current}.{i}"
            dst = f"{self.current}.{i+1}"
            if os.path.exists(src):
                os.replace(src, dst)
        os.replace(self.current, f"{self.current}.1")
        self._open_file()

    def read_logs(self, start, end, sensor_id=None):
        raise NotImplementedError("Czytanie historii logów nie zostało zaimplementowane.")
