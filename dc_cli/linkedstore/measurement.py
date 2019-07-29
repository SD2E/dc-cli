import logging
from . import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class Measurement:
    collection = 'measurement'
    collection_name = 'Measurement'
    display_fields = [
        'uuid', 'measurement_id', 'measurement_name', 'measurement_type']
    id_fields = ['uuid', 'measurement_id']
    lst_defs = [
        ('id', 'measurement_id', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('type', 'measurement_type', searchtypes.STRING,
         searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('name', 'measurement_name', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN]),
        ('group_id', 'measurement_group_id', searchtypes.STRING,
         searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN]),
        ('timepoint', 'timepoint.value', searchtypes.FLOAT,
         searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN])]


class MeasurementList(Measurement, CollectionList):
    """
    List measurements
    """
    # collection = 'measurement'
    log = logging.getLogger(__name__)


class MeasurementShow(Measurement, CollectionMember):
    """
    Show one measurement
    """
    log = logging.getLogger(__name__)
