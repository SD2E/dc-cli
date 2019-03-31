from attrdict import AttrDict


class DataCatalogRecord(AttrDict):

    fields = []

    @classmethod
    def set_fields(cls, field_names=[]):
        setattr(cls, 'fields', field_names)

    def as_list(self):
        resp = list()
        for f in self.fields:
            if f != '_id':
                resp.append(self.get(f, None))
        return resp
