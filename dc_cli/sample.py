import logging
from .collections import CollectionList


class SampleList(CollectionList):
    collection = 'sample'
    log = logging.getLogger(__name__)
    displayfields = ['uuid', 'lab_sample_id']
