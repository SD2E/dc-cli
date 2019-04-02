import logging
from .collections import CollectionList, CollectionMember


class ExperimentDesign:
    collection = 'experiment_design'
    identifier_name = 'uuid or experiment_design_id'


class ExperimentDesignList(ExperimentDesign, CollectionList):
    """
    List experiment requests/designs
    """
    log = logging.getLogger(__name__)


class ExperimentDesignGet(ExperimentDesign, CollectionMember):
    """
    Show one experiment request/design
    """
    log = logging.getLogger(__name__)
