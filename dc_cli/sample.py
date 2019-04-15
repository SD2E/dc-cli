import logging
from .collections import (CollectionList, CollectionMember, searchmods)


class Sample:
    collection = 'sample'
    collection_name = 'Sample'
    display_fields = ['uuid', 'lab_sample_id']
    id_fields = ['uuid', 'sample_id']
    lst_defs = [
        ('id', 'sample_id', searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('labid', 'lab_sample_id', searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('control_type', 'control_type', searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN]),
        ('replicate', 'replicate', searchmods.EQUALS,
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
