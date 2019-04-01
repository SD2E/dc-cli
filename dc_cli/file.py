import logging
from .collections import CollectionList


class FileList(CollectionList):
    collection = 'file'
    log = logging.getLogger(__name__)
