import logging
from .collections import CollectionList, CollectionMember


class Measurement:
    collection = 'measurement'
    collection_name = 'Measurement'
    display_fields = [
        'uuid', 'measurement_id', 'measurement_name', 'measurement_type']
    id_fields = ['uuid', 'measurement_id']


class MeasurementList(Measurement, CollectionList):
    """
    List measurements
    """
    # collection = 'measurement'
    log = logging.getLogger(__name__)


class MeasurementShow(Measurement, CollectionMember):
    """
    Show one measurement
    """
    log = logging.getLogger(__name__)
