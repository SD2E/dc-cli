import logging
from .collections import CollectionList


class Sample:
    collection = 'sample'
    displayfields = ['uuid', 'lab_sample_id']


class SampleList(Sample, CollectionList):
    """
    List samples
    """
    log = logging.getLogger(__name__)
