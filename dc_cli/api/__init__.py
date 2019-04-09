import logging
from .mongo import DatabaseAPI, Verbosity
from .agave import AbacoAPI, AgaveAPI, AgaveError
from .record import DataCatalogRecord
from .pipelinejobs import PipelineJobEvent

try:  # Python 2.7
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())
