import logging
from .collections import CollectionList


class File:
    collection = 'file'


class FileList(File, CollectionList):
    """
    List managed files
    """
    log = logging.getLogger(__name__)
