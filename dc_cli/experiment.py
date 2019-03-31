import logging
from .collections import CollectionList


class ExperimentList(CollectionList):
    collection = 'experiment'
    log = logging.getLogger(__name__)
