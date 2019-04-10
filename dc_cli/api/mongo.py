import logging
from .. import settings
from datacatalog.managers import Manager
from datacatalog.identifiers import typeduuid
from .record import DataCatalogRecord


class Verbosity:
    IDENTIFIERS = 0
    INDEXED = 1
    ALL = 2
    DEFAULT = INDEXED


FILTERED_FIELDS = ['experiment_designs', 'experiments',
                   'samples', 'measurements', 'files', 'jobs']


class DatabaseAPI(object):
    """Basic class for accessing a Data Catalog via its MongoDB connection

    Args:
        verbose (bool): Whether to return complete or summary responses
    """

    log = logging.getLogger(__name__)

    def __init__(self, mongo_host=settings.MONGODB_HOST,
                 mongo_port=settings.MONGODB_PORT,
                 mongo_database=settings.MONGODB_DATABASE,
                 mongo_username=settings.MONGODB_USERNAME,
                 mongo_password=settings.MONGODB_PASSWORD,
                 api_server=settings.TACC_API_SERVER,
                 api_token=None,
                 fields=None,
                 flatten=False,
                 verbose=Verbosity.INDEXED):

        self.log.debug('Initializing MongoDB API')

        mongodb = {'host': mongo_host, 'port': mongo_port,
                   'database': mongo_database, 'username': mongo_username,
                   'password': mongo_password}

        self.verbosity = verbose
        self.flatten = flatten
        self.display_fields = fields
        self.db = Manager(mongodb)
        self.log.debug('(Initialized)')

    def get_identifiers(self, name):
        """Retrieve fields that are identifiers in a collection
        """
        return self.db.stores[name].get_indexes()

    def get_fieldnames(self, name, filter=[], humanize=False):
        """Dynamically get field names for display in CLI

        The function either inspects the schema for a given collection
        and makes an informed guess on which elements are amenable to
        display or relies on values provided in self.display_fields
        """
        fieldnames = None
        if self.verbosity == Verbosity.ALL:
            fieldnames = self.db.stores[name].get_fields()
        elif self.verbosity == Verbosity.INDEXED:
            if self.display_fields is not None:
                fieldnames = self.display_fields
            else:
                fieldnames = self.db.stores[name].get_indexes()
        else:
            fieldnames = self.db.stores[name].get_identifiers()
        self.log.debug('Field Names: {}'.format(fieldnames))

        for f in FILTERED_FIELDS:
            try:
                fieldnames.remove(f)
            except ValueError:
                pass

        if humanize:
            fieldnames = [f.title() for f in fieldnames]

        return fieldnames

    def query_collection(self, name, filter={}, limit=None,
                         skip=None, raw=False):
        """Run a MongoDB query in JSON format against a specific named collection
        """
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
                if raw:
                    yield r
                else:
                    yield DataCatalogRecord(r).as_list()

    def get_by_identifier(self, identifier, raw=False):
        """Fetch the MongoDB record for any indexed identifier
        """
        resp = self.db.get_by_identifier(identifier, permissive=False)
        self.log.debug('Response: {}'.format(resp))
        if resp is not None:
            if raw:
                return resp
            else:
                resp_type = typeduuid.get_uuidtype(resp['uuid'])
                filt_fields = self.get_fieldnames(resp_type, humanize=False)
                DataCatalogRecord.set_flatten(self.flatten)
                DataCatalogRecord.set_fields(filt_fields)
                return DataCatalogRecord(resp).as_list()

    def get_collection_member_by_identifier(self, identifier,
                                            collection=None, raw=False):
        """Fetch the MongoDB record for any indexed identifier from a collection
        """
        self.log.debug('Ident, Coll: {}, {}'.format(identifier, collection))
        if collection is None:
            return self.get_by_identifier(identifier)
        resp = self.db.stores[collection].find_one_by_identifier(identifier)
        self.log.debug('Response: {}'.format(resp))
        if resp is not None:
            if raw:
                return resp
            else:
                resp_type = typeduuid.get_uuidtype(resp['uuid'])
                filt_fields = self.get_fieldnames(resp_type, humanize=False)
                DataCatalogRecord.set_flatten(self.flatten)
                DataCatalogRecord.set_fields(filt_fields)
                return DataCatalogRecord(resp).as_list()

    def get_uuid_type(self, uuid):
        """Return the TypedUUID type for this class or subclass"""
        return typeduuid.get_uuidtype(uuid)


def ordered_projection(fields):
    """Creates a MongoDB projection from an ordered list of fields"""
    if not isinstance(fields, list):
        if isinstance(fields, tuple):
            fields = list(fields)
        elif isinstance(fields, (str, int, float, bool)):
            fields = [fields]
    return {fields[i]: (i+1) for i in range(0, len(fields))}
