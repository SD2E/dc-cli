import logging
from .collections import CollectionList, CollectionMember


class File:
    collection = 'file'


class FileList(File, CollectionList):
    """
    List managed files
    """
    log = logging.getLogger(__name__)


class FileGet(File, CollectionMember):
    """
    Show one file
    """
    log = logging.getLogger(__name__)
