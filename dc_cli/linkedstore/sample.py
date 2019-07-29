import logging
from . import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class Sample:
    collection = 'sample'
    collection_name = 'Sample'
    display_fields = ['uuid', 'lab_sample_id']
    id_fields = ['uuid', 'sample_id']
    lst_defs = [
        ('id', 'sample_id', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('labid', 'lab_sample_id', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('control_type', 'control_type', searchtypes.STRING,
         searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN]),
        ('replicate', 'replicate', searchtypes.INTEGER,
         searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN])]


class SampleList(Sample, CollectionList):
    """
    List samples
    """
    log = logging.getLogger(__name__)


class SampleShow(Sample, CollectionMember):
    """
    Show one sample
    """
    log = logging.getLogger(__name__)
