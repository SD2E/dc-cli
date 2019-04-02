import logging
from .collections import CollectionList, CollectionMember


class Sample:
    collection = 'sample'
    displayfields = ['uuid', 'lab_sample_id']


class SampleList(Sample, CollectionList):
    """
    List samples
    """
    log = logging.getLogger(__name__)


class SampleGet(Sample, CollectionMember):
    """
    Show one sample
    """
    log = logging.getLogger(__name__)
