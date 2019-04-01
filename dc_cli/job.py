import logging
from .collections import CollectionList


class JobList(CollectionList):
    collection = 'pipelinejob'
    log = logging.getLogger(__name__)
    displayfields = ['uuid', 'state', 'updated']
