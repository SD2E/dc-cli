import logging
from .collections import CollectionList


class Measurement:
    collection = 'measurement'
    displayfields = ['uuid', 'measurement_type', 'measurement_name']


class MeasurementList(Measurement, CollectionList):
    """
    List measurements
    """
    # collection = 'measurement'
    log = logging.getLogger(__name__)
