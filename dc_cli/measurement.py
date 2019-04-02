import logging
from .collections import CollectionList, CollectionMember


class Measurement:
    collection = 'measurement'
    displayfields = ['uuid', 'measurement_type', 'measurement_name']


class MeasurementList(Measurement, CollectionList):
    """
    List measurements
    """
    # collection = 'measurement'
    log = logging.getLogger(__name__)


class MeasurementGet(Measurement, CollectionMember):
    """
    Show one measurement
    """
    log = logging.getLogger(__name__)
