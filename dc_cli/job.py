import logging
from .collections import CollectionList


class Job:
    collection = 'pipelinejob'
    displayfields = ['uuid', 'state', 'updated']


class JobList(Job, CollectionList):
    """
    List pipeline jobs
    """
    log = logging.getLogger(__name__)
