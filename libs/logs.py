import json
import logging
import sys
from typing import Literal, Union

LOG_LEVEL = Union[
    Literal['INFO'],
    Literal['WARN'],
    Literal['ERROR'],
]

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        return json.dumps(vars(record))


class JsonLogger(logging.Logger):
    def __init__(self, name, level):
        super().__init__(name, level)
    
    def makeRecord(self, name, lvl, fn, lno, msg, args, exc_info, func, extra, sinfo):
        return super().makeRecord(name, lvl, fn, lno, msg, args, exc_info, func, extra, sinfo)


def get_logger(name, level: LOG_LEVEL='INFO') -> JsonLogger:
    if level not in ('INFO', 'WARN', 'ERROR'):
        raise ValueError('invalid log level')
    loglevel = getattr(logging, level)
    log = JsonLogger(name, level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    for h in log.handlers:
        log.removeHandler(h)
    log.addHandler(handler)
    return log
