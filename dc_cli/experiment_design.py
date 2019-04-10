import logging
from .collections import CollectionList, CollectionMember


class ExperimentDesign:
    collection = 'experiment_design'
    collection_name = 'Experiment Design'
    display_fields = ['uuid', 'experiment_design_id',
                      'title', 'status', 'updated']
    id_fields = ['uuid', 'experiment_design_id']


class ExperimentDesignList(ExperimentDesign, CollectionList):
    """
    List experiment requests/designs
    """
    log = logging.getLogger(__name__)


class ExperimentDesignShow(ExperimentDesign, CollectionMember):
    """
    Show one experiment request/design
    """
    log = logging.getLogger(__name__)
