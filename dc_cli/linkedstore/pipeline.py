from collections import namedtuple
import logging
from . import (
    CollectionList, CollectionMember, searchmods, searchtypes)

PipelineRecord = namedtuple('Pipeline', 'uuid name id')


class Pipeline:
    collection = 'pipeline'
    collection_name = 'Pipeline'
    display_fields = ['uuid', 'name']
    id_fields = ['uuid']
    lst_defs = [('name', 'name', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.STARTS_WITH, searchmods.ENDS_WITH,
                  searchmods.LIKE, searchmods.NOT_LIKE]),
                ('description', 'description', searchtypes.STRING,
                 searchmods.LIKE,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN])]


class PipelineList(Pipeline, CollectionList):
    """
    List pipelines
    """
    log = logging.getLogger(__name__)


class PipelineShow(Pipeline, CollectionMember):
    """
    Show one pipeline
    """
    log = logging.getLogger(__name__)
