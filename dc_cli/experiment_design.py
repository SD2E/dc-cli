import logging
from .collections import CollectionList


class ExperimentDesignList(CollectionList):
    collection = 'experiment_design'
    log = logging.getLogger(__name__)
