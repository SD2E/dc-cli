import logging
from .collections import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class ExperimentDesign:
    collection = 'experiment_design'
    collection_name = 'Experiment Design'
    display_fields = ['uuid', 'experiment_design_id',
                      'title', 'status', 'updated']
    id_fields = ['uuid', 'experiment_design_id']
    lst_defs = [('status', 'status', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN]),
                ('title', 'title', searchtypes.STRING,
                 searchmods.LIKE,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.LIKE, searchmods.NOT_LIKE,
                  searchmods.IN, searchmods.NOT_IN]),
                ('id', 'experiment_design_id', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN,
                  searchmods.LIKE, searchmods.NOT_LIKE]),
                ('created', 'created', searchtypes.DATETIME,
                 searchmods.ON,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.GREATER_THAN, searchmods.GREATER_THAN_EQUAL,
                  searchmods.LESS_THAN, searchmods.LESS_THAN_EQUAL,
                  searchmods.ON, searchmods.AFTER, searchmods.BEFORE]),
                ('updated', 'updated', searchtypes.DATETIME,
                 searchmods.ON,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.GREATER_THAN, searchmods.GREATER_THAN_EQUAL,
                  searchmods.LESS_THAN, searchmods.LESS_THAN_EQUAL,
                  searchmods.ON, searchmods.AFTER, searchmods.BEFORE])]


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
