import os
# from funcy import distinct, remove
from .helpers import (fix_assets_path, array_from_string, parse_boolean,
                      int_or_none, set_from_string)

from .organization import *
from .debug import *
from ..import utils


def all_settings():
    from types import ModuleType

    settings = {}
    for name, item in globals().iteritems():
        if not callable(item) and not name.startswith("__") and not isinstance(item, ModuleType):
            settings[name] = item
    return settings


ADMIN_TOKEN_KEY = utils.env('ADMIN_TOKEN_KEY')

JOB_MANAGER_ID = utils.env('JOB_MANAGER_ID')
JOB_MANAGER_NONCE = utils.env('JOB_MANAGER_NONCE')
JOB_INDEXER_ID = utils.env('JOB_INDEXER_ID')
JOB_INDEXER_NONCE = utils.env('JOB_INDEXER_NONCE')

LOGLEVEL = utils.env('LOGLEVEL')

MONGODB_HOST = utils.env('MONGODB_HOST')
MONGODB_PORT = utils.env('MONGODB_PORT', cast=int)
MONGODB_DATABASE = utils.env('MONGODB_DATABASE')
MONGODB_USERNAME = utils.env('MONGODB_USERNAME')
MONGODB_PASSWORD = utils.env('MONGODB_PASSWORD')

PAGESIZE = utils.env('PAGESIZE', cast=int)
REACTOR_MESSAGE_SYNC = utils.env('REACTOR_MESSAGE_SYNC', cast=bool)
