import logging
from . import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class Experiment:
    collection = 'experiment'
    display_fields = ['uuid', 'experiment_id', 'title']
    # identifier_name = 'uuid or experiment_id'
    collection_name = 'Experiment'
    id_fields = ['uuid', 'experiment_id']
    lst_defs = [
        ('id', 'experiment_id', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('title', 'title', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN])]


class ExperimentList(Experiment, CollectionList):
    """
    List experiments
    """
    log = logging.getLogger(__name__)


class ExperimentShow(Experiment, CollectionMember):
    """
    Show one experiment
    """
    log = logging.getLogger(__name__)
