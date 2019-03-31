import json
import logging
from .constants import (MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE,
                        MONGODB_USERNAME, MONGODB_PASSWORD,
                        API_SERVER, API_TOKEN, PAGESIZE)
from datacatalog.managers import Manager
from .record import DataCatalogRecord


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
                 verbose=False):

        mongodb = {'host': mongo_host, 'port': mongo_port,
                   'database': mongo_database, 'username': mongo_username,
                   'password': mongo_password}

        self.log = logging.getLogger(__name__)
        self.verbose = verbose
        self.db = Manager(mongodb)

    def get_fieldnames(self, name, filter=[]):

        if self.verbose:
            return self.db.stores[name].get_fields()
        else:
            return self.db.stores[name].get_identifiers()

    def query_collection(self, name, filter={}, page=0):
        fields = self.get_fieldnames(name)
        proj = ordered_projection(fields)
        resp = self.db.stores[name].query(filter, projection=proj)
        if resp is not None:
            DataCatalogRecord.set_fields(fields)
            for r in resp:
                yield DataCatalogRecord(r).as_list()


def ordered_projection(fields):
    """Creates a MongoDB projection from an ordered list of fields"""
    if not isinstance(fields, list):
        if isinstance(fields, tuple):
            fields = list(fields)
        elif isinstance(fields, (str, int, float, bool)):
            fields = [fields]
    return {fields[i]: (i+1) for i in range(0, len(fields))}
