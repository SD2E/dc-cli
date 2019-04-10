import logging
from .collections import CollectionList, CollectionMember


class Sample:
    collection = 'sample'
    collection_name = 'Sample'
    display_fields = ['uuid', 'lab_sample_id']
    id_fields = ['uuid', 'sample_id']


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
