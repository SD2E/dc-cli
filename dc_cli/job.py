import logging
from .collections import CollectionList, CollectionMember


class Job:
    collection = 'pipelinejob'
    displayfields = ['uuid', 'state', 'updated']


class JobList(Job, CollectionList):
    """
    List pipeline jobs
    """
    log = logging.getLogger(__name__)


class JobGet(Job, CollectionMember):
    """
    Show one pipeline job
    """
    log = logging.getLogger(__name__)
