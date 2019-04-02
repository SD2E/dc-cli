import logging
from attrdict import AttrDict


class DataCatalogRecord(AttrDict):

    fields = []
    log = logging.getLogger(__name__)

    @classmethod
    def set_fields(cls, field_names=[]):
        setattr(cls, 'fields', field_names)

    def as_list(self):
        self.log.debug('Self: {}'.format(self))
        resp = list()
        for f in self.fields:
            self.log.debug('Field:Value {}:{}'.format(f, self.get(f)))
            if f != '_id':
                resp.append(self.get(f, None))
        self.log.debug('As List: {}'.format(resp))
        return resp
