import logging
from attrdict import AttrDict
from .utils import flatten_json


class DataCatalogRecord(AttrDict):
    """Container and formatted class for Data Catalog records
    """
    fields = []
    log = logging.getLogger(__name__)
    flatten = False

    @classmethod
    def set_fields(cls, field_names=[]):
        setattr(cls, 'fields', field_names)

    @classmethod
    def set_flatten(cls, flatten):
        setattr(cls, 'flatten', flatten)

    def as_list(self):
        self.log.debug('Self: {}'.format(self))
        resp = list()
        for f in self.fields:
            self.log.debug('Field:Value {}:{}'.format(f, self.get(f)))
            if f != '_id':
                val = self.get(f, None)
                if self.flatten and isinstance(val, (dict, list)):
                    self.log.debug('Flattening {}'.format(f))
                    val = flatten_json(val)
                resp.append(val)
        self.log.debug('As List: {}'.format(resp))
        return resp
