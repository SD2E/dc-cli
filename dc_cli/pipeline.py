import logging
from .collections import (CollectionList, CollectionMember, searchmods)
from collections import namedtuple

PipelineRecord = namedtuple('Pipeline', 'uuid name id')


class Pipeline:
    collection = 'pipeline'
    collection_name = 'Pipeline'
    display_fields = ['uuid', 'name', 'description']
    id_fields = ['uuid']
    lst_defs = [('name', 'name', searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.STARTS_WITH, searchmods.ENDS_WITH,
                  searchmods.LIKE, searchmods.NOT_LIKE]),
                ('description', 'description', searchmods.LIKE,
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
