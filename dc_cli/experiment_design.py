import logging
from .collections import CollectionList


class ExperimentDesign:
    collection = 'experiment_design'


class ExperimentDesignList(ExperimentDesign, CollectionList):
    """
    List experiment requests/designs
    """
    log = logging.getLogger(__name__)
