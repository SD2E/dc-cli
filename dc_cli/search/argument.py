import arrow
import dateparser
import inflection
from datetime import datetime
from attrdict import AttrDict
from bson.regex import Regex
from collections import namedtuple
from . import searchmods, searchtypes

BOOLEAN_TRUE_STRINGS = ('true', 'on', 'ok', 'y', 'yes', '1')
DATETIME = 'datetime'

Argument = namedtuple('Argument', 'argument, attributes')


class MongoQuery(dict):
    pass


class ArrowSpan(arrow.Arrow):
    """Subclass of Arrow with upgraded span() capability used to
    generate MongoDB date ranges for queries
    """
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'
    MINUTE = 'minute'
    SPANS = [YEAR, MONTH, WEEK, DAY, HOUR, MINUTE]
    default_span = DAY
    original_value = None

    def setup(self, value):
        setattr(self, 'original_value', value)
        return self

    def smart_span(self, span_value=None):
        orig = getattr(self, 'original_value', '').lower()
        span = self.default_span
        if span_value is None:
            # Iterate thru last X, this X, next X, etc
            for s in [self.YEAR, self.MONTH, self.WEEK, self.DAY]:
                if s in orig:
                    span = s
                    break
        # We are able to call Arrow's span() since this is a subclass
        return self.span(span)

    def smart_floor(self, span_value=None):
        orig = getattr(self, 'original_value', '').lower()
        span = self.default_span
        if span_value is None:
            # Iterate thru last X, this X, next X, etc
            for s in [self.YEAR, self.MONTH, self.WEEK, self.DAY]:
                if s in orig:
                    span = s
                    break
        # We are able to call Arrow's floor() since this is a subclass
        return self.floor(span).datetime

    def smart_ceil(self, span_value=None):
        orig = getattr(self, 'original_value', '').lower()
        span = self.default_span
        if span_value is None:
            # Iterate thru last X, this X, next X, etc
            for s in [self.YEAR, self.MONTH, self.WEEK, self.DAY]:
                if s in orig:
                    span = s
                    break
        # We are able to call Arrow's ceil()) since this is a subclass
        return self.ceil(span).datetime


class SearchArg(object):
    """Encapsulates argparse formatting and translation to MongoDB queries
    """
    PARAMS = [
        ('argument', True, 'argument', 'str', None),
        ('field', False, 'field', 'str', None),
        ('choices', False, 'choices', None, None),
        ('mods', False, 'mods', 'list', [searchmods.EQUALS]),
        ('default_mod', False, 'default_mod', 'str', searchmods.EQUALS)]

    def __init__(self, field_type=searchtypes.STRING, inflect=True, **kwargs):
        setattr(self, 'field_type', field_type)
        setattr(self, 'inflection', inflect)
        for param, required, attr, typ, default in self.PARAMS:
            val = kwargs.get(param, default)
            if required:
                if param not in kwargs:
                    raise ValueError(
                        'Parameter "{}" is required'.format(param))
            setattr(self, attr, val)

        if self.field is None:
            self.field = self.argument

        if self.inflection:
            self.argument = inflection.parameterize(
                self.argument, separator='-').replace('_', '-')

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
        """Generate a PyMongo query for an argument and its value(s)
        """
        modifier = None
        # Base assumption: first element is search modifier. Otherwise, use
        # default, allowing for --flag <value> behavior
        if len(values) == 2:
            modifier = values[0]
            values.remove(values[0])
        elif modifier is None:
            modifier = self.default_mod
        # Now, type-cast values as per SearchArg.field_type
        casted_values = [self.cast(v) for v in values]
        if modifier in self.mods:
            fn = getattr(self, 'query_' + modifier)
            return fn(casted_values)
        else:
            raise ValueError('"{}" is not a valid modifier for "{}"'.format(
                modifier, self.argument))

    def cast(self, value, field_type=None):
        """Cast a value into a defined Python type
        """
        if field_type is None:
            field_type = self.field_type
        if value:
            # human-provided date string => Python datetime(s)
            if field_type is DATETIME:
                # orig_val = value
                value = self.parse_datetime(value)
                # value.setup(orig_val)
                return value
            # human-provided boolean => Python bool
            elif field_type is bool:
                value = value.lower() in BOOLEAN_TRUE_STRINGS
                return value
            # Fall back to generic Python casting behavior
            try:
                return field_type(value)
            except ValueError:
                raise Exception(
                    'Unable to cast {} to {}'.format(value, field_type))

    @classmethod
    def parse_datetime(cls, value, span=None):
        """Transform a human date or time string to a Python UTC datetime
        """
        factory = arrow.ArrowFactory(ArrowSpan)
        dta = factory.get(dateparser.parse(
            value, settings={'TIMEZONE': 'UTC'}))
        dta.setup(value)
        return dta

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

        qvals = [self.cast(q) for q in qvals]
        return qvals

    def query_eq(self, value):
        # EQUALS
        if isinstance(value, list):
            value = value[0]
        if self.field_type is searchtypes.DATETIME:
            return MongoQuery({self.field: {'$gte': value.smart_floor(),
                                            '$lt': value.smart_ceil()}})
        else:
            return MongoQuery({self.field: value})

    def query_neq(self, value):
        # NOT_EQUAL
        if isinstance(value, list):
            value = value[0]
        if self.field_type is searchtypes.DATETIME:
            return MongoQuery({self.field: {'$not': {
                '$gte': value.smart_floor(),
                '$lt': value.smart_ceil()}}})
        else:
            return MongoQuery({self.field: {'$ne': value}})

    def query_gt(self, value):
        # GREATER_THAN
        if isinstance(value, list):
            value = value[0]
        if self.field_type is searchtypes.DATETIME:
            value = value.datetime
        return MongoQuery({self.field: {'$gt': value}})

    def query_gte(self, value):
        # GREATER_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        if self.field_type is searchtypes.DATETIME:
            value = value.datetime
        return MongoQuery({self.field: {'$gte': value}})

    def query_lt(self, value):
        # LESS_THAN
        if isinstance(value, list):
            value = value[0]
        if self.field_type is searchtypes.DATETIME:
            value = value.datetime
        return MongoQuery({self.field: {'$lt': value}})

    def query_lte(self, value):
        # LESS_THAN_OR_EQUAL
        if isinstance(value, list):
            value = value[0]
        if self.field_type is searchtypes.DATETIME:
            value = value.datetime
        return MongoQuery({self.field: {'$lte': value}})

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

    def query_on(self, value):
        if self.field_type is not searchtypes.DATETIME:
            raise TypeError('"on" may only be used for dates and times')
        return self.query_eq(value)

    def query_after(self, value):
        if self.field_type is not searchtypes.DATETIME:
            raise TypeError('"after" may only be used for dates and times')
        return self.query_gt(value)

    def query_before(self, value):
        if self.field_type is not searchtypes.DATETIME:
            raise TypeError('"before" may only be used for dates and times')
        return self.query_lt(value)
