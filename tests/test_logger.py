# tests/test_logger.py
import json
from datetime import datetime
from logger.logger import Logger

def test_logger_rotation(tmp_path):
    cfg = tmp_path / 'config.json'
    cfg.write_text(json.dumps({
        'log_dir': str(tmp_path),
        'filename_pattern': 'test.csv',
        'max_size_mb': 0.0001,
        'backup_count': 2,
        'buffer_size': 1
    }))
    log = Logger(str(cfg))
    log.log_reading('s', datetime.now(), 1.0, 'u')
    log.log_reading('s', datetime.now(), 2.0, 'u')
    files = list(tmp_path.glob('test.csv*'))
    assert len(files) <= 2