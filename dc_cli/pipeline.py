import logging
from .collections import CollectionList


class Pipeline:
    collection = 'pipeline'
    displayfields = ['uuid', 'name', 'description']


class PipelineList(Pipeline, CollectionList):
    """
    List pipelines
    """
    log = logging.getLogger(__name__)
