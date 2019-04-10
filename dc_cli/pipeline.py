import logging
from .collections import CollectionList, CollectionMember
from collections import namedtuple

PipelineRecord = namedtuple('Pipeline', 'uuid name id')


class Pipeline:
    collection = 'pipeline'
    collection_name = 'Pipeline'
    display_fields = ['uuid', 'name', 'description']
    id_fields = ['uuid']


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
