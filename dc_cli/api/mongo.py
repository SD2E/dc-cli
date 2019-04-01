import json
import logging
from .constants import (MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE,
                        MONGODB_USERNAME, MONGODB_PASSWORD,
                        API_SERVER, API_TOKEN, PAGESIZE)
from datacatalog.managers import Manager
from .record import DataCatalogRecord


class Verbosity:
    IDENTIFIERS = 0
    INDEXED = 1
    ALL = 2
    DEFAULT = INDEXED


FILTERED_FIELDS = ['experiment_designs', 'experiments',
                   'samples', 'measurements', 'files', 'jobs']


class DatabaseAPI(object):
    """Main class for accessing a Data Catalog via MongoDB connection

    Args:
        verbose (bool): Whether to return complete or summary responses
    """

    def __init__(self, mongo_host=MONGODB_HOST,
                 mongo_port=MONGODB_PORT,
                 mongo_database=MONGODB_DATABASE,
                 mongo_username=MONGODB_USERNAME,
                 mongo_password=MONGODB_PASSWORD,
                 api_server=API_SERVER,
                 api_token=API_TOKEN,
                 fields=None,
                 verbose=Verbosity.INDEXED):

        mongodb = {'host': mongo_host, 'port': mongo_port,
                   'database': mongo_database, 'username': mongo_username,
                   'password': mongo_password}

        self.log = logging.getLogger(__name__)
        self.verbosity = verbose
        self.displayfields = fields
        self.db = Manager(mongodb)

    def get_fieldnames(self, name, filter=[], humanize=False):

        fieldnames = None
        if self.verbosity == Verbosity.ALL:
            fieldnames = self.db.stores[name].get_fields()
        elif self.verbosity == Verbosity.INDEXED:
            if self.displayfields is not None:
                fieldnames = self.displayfields
            else:
                fieldnames = self.db.stores[name].get_indexes()
        else:
            fieldnames = self.db.stores[name].get_identifiers()

        for f in FILTERED_FIELDS:
            try:
                fieldnames.remove(f)
            except ValueError:
                pass

        if humanize:
            fieldnames = [f.title() for f in fieldnames]

        return fieldnames

    def query_collection(self, name, filter={}, limit=None, skip=None):
        fields = self.get_fieldnames(name)
        proj = ordered_projection(fields)
        extras = dict()
        if limit is not None:
            extras['limit'] = int(limit)
        if skip is not None:
            extras['skip'] = int(skip)
        resp = self.db.stores[name].query(
            filter, projection=proj, **extras)
        if resp is not None:
            DataCatalogRecord.set_fields(fields)
            for r in resp:
                yield DataCatalogRecord(r).as_list()

    def get_by_identifier(self):
        fields = self.get_fieldnames(name)
        proj = ordered_projection(fields)
        extras = dict()
        pass


def ordered_projection(fields):
    """Creates a MongoDB projection from an ordered list of fields"""
    if not isinstance(fields, list):
        if isinstance(fields, tuple):
            fields = list(fields)
        elif isinstance(fields, (str, int, float, bool)):
            fields = [fields]
    return {fields[i]: (i+1) for i in range(0, len(fields))}
