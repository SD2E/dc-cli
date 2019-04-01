import logging
from .collections import CollectionList


class MeasurementList(CollectionList):
    collection = 'measurement'
    log = logging.getLogger(__name__)
