import logging
from .collections import CollectionList, CollectionMember
from collections import namedtuple

PipelineRecord = namedtuple('Pipeline', 'uuid name id')


class Pipeline:
    collection = 'pipeline'
    displayfields = ['uuid', 'name', 'description']


class PipelineList(Pipeline, CollectionList):
    """
    List pipelines
    """
    log = logging.getLogger(__name__)


class PipelineGet(Pipeline, CollectionMember):
    """
    Show one pipeline
    """
    log = logging.getLogger(__name__)
