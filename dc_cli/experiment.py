import logging
from .collections import CollectionList


class Experiment:
    collection = 'experiment'


class ExperimentList(Experiment, CollectionList):
    """
    List experiments
    """
    log = logging.getLogger(__name__)
