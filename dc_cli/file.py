import logging
from .collections import CollectionList, CollectionMember
from .tapis import TapisShowOne, TapisError


class File:
    collection = 'file'


class FileList(File, CollectionList):
    """
    List managed files
    """
    log = logging.getLogger(__name__)


class FileShow(File, CollectionMember):
    """
    Show one file by identifier
    """
    log = logging.getLogger(__name__)


class FileGet(File, TapisShowOne):
    """
    Download a file by identifier
    """
    log = logging.getLogger(__name__)
