import logging
from .collections import CollectionList, CollectionMember


class Challenge:
    collection = 'challenge_problem'
    collection_name = 'Challenge Problem'
    display_fields = ['uuid', 'id', 'title', 'status', 'updated']
    id_fields = ['uuid', 'id']


class ChallengeList(Challenge, CollectionList):
    """
    List challenge problems
    """
    log = logging.getLogger(__name__)


class ChallengeGet(Challenge, CollectionMember):
    """
    Get one challenge problem
    """
    log = logging.getLogger(__name__)
