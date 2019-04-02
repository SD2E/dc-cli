import logging
from .collections import CollectionList, CollectionMember


class Experiment:
    collection = 'experiment'
    displayfields = ['uuid', 'experiment_id', 'title']
    identifier_name = 'uuid or experiment_id'


class ExperimentList(Experiment, CollectionList):
    """
    List experiments
    """
    log = logging.getLogger(__name__)


class ExperimentGet(Experiment, CollectionMember):
    """
    Show one experiment
    """
    log = logging.getLogger(__name__)
