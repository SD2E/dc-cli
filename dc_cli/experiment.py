import logging
from .collections import CollectionList


class Experiment:
    collection = 'experiment'
    displayfields = ['uuid', 'experiment_id', 'title']


class ExperimentList(Experiment, CollectionList):
    """
    List experiments
    """
    log = logging.getLogger(__name__)
