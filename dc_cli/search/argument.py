from attrdict import AttrDict
from bson.regex import Regex
from collections import namedtuple
from . import searchmods


Argument = namedtuple('Argument', 'argument, attributes')


class MongoQuery(dict):
    pass


class SearchArg(object):
    """Encapsulates argparse formatting and translation to MongoDB queries
    """
    PARAMS = [
        ('argument', True, 'argument', str, None),
        ('field', False, 'field', str, None),
        ('choices', False, 'choices', None, None),
        ('mods', False, 'mods', list, [searchmods.EQUALS]),
        ('default_mod', False, 'default_mod', str, searchmods.EQUALS)]

    def __init__(self, **kwargs):
        for param, required, attr, typ, default in self.PARAMS:
            val = kwargs.get(param, default)
            if required:
                if param not in kwargs:
                    raise ValueError(
                        'Parameter "{}" is required'.format(param))
                if typ is not None:
                    assert isinstance(
                        val, typ), '{}.{} must be type "{}"'.format(
                            param, val, typ)
            setattr(self, attr, val)

        if self.field is None:
            self.field = self.argument

    def argparse(self):
        """Generate an argparse argument for a MongoDB collection field
        """
        params = {
            'nargs': '+',
            'metavar': ('[mod]', 'VALUE')}
        if self.choices is not None:
            params['choices'] = self.choices
        return Argument('--' + self.argument, params)

    def get_query(self, values):
        """Generate a PyMongo query for an argument and its value
        """
        modifier = None
        # first element is assumed to be the search modifier
        if len(values) == 2:
            modifier = values[0]
            values.remove(values[0])
        elif modifier is None:
            modifier = self.default_mod
        if modifier in self.mods:
            fn = getattr(self, 'query_' + modifier)
            return fn(values)
        else:
            raise ValueError('"{}" is not a valid modifier for "{}"'.format(
                modifier, self.argument))

    def to_values(self, value, delim=','):
        """Transform a value into a list of values
        """
        qvals = list()
        if isinstance(value, list):
            return value
        elif isinstance(value, tuple):
            return list(value)
        elif isinstance(value, (bool, int, float)):
            return [value]
        elif isinstance(value, str):
            qvals = value.split(delim)
            qvals = [q.strip() for q in qvals]
        return qvals

    def query_eq(self, value):
        # EQUALS
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: value})

    def query_neq(self, value):
        # NOT_EQUAL
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: {'$ne': value}})

    def query_gt(self, value):
        # GREATER_THAN
        pass

    def query_gte(self, value):
        # GREATER_THAN_OR_EQUAL
        pass

    def query_lt(self, value):
        # LESS_THAN
        pass

    def query_lte(self, value):
        # LESS_THAN_OR_EQUAL
        pass

    def query_in(self, values):
        # IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        return MongoQuery({self.field: {'$in': qvals}})

    def query_nin(self, values):
        # NOT IN (array)
        if not isinstance(values, list):
            values = [values]
        qvals = self.to_values(values)
        return MongoQuery({self.field: {'$nin': qvals}})

    def query_start(self, value):
        # STARTS WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: Regex('^' + value + '.*', 'i')})

    def query_nstart(self, value):
        # DOESN'T START WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: {'$not': Regex(
            '^' + value + '.*', 'i')}})

    def query_end(self, value):
        # ENDS WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: Regex('*.' + value + '$', 'i')})

    def query_nend(self, value):
        # DOESN'T END WITH
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: {'$not': Regex(
            '*.' + value + '$', 'i')}})

    def query_like(self, value):
        # WILDCARD CONTAINS
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: Regex('.*' + value + '.*', 'i')})

    def query_nlike(self, value):
        # WILDCARD NOT CONTAINS
        if isinstance(value, list):
            value = value[0]
        return MongoQuery({self.field: {'$not': Regex(
            '.*' + value + '.*', 'i')}})
