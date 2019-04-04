import logging
from .mongo import DatabaseAPI, Verbosity
from .agave import AgaveAPI, AgaveError

try:  # Python 2.7
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
