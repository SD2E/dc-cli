import logging
from .collections import CollectionList


class PipelineList(CollectionList):
    collection = 'pipeline'
    log = logging.getLogger(__name__)
