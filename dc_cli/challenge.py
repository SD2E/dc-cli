import logging
from .collections import CollectionList, CollectionMember


class Challenge:
    collection = 'challenge_problem'
    displayfields = ['uuid', 'id', 'title', 'status', 'updated']
    identifier_name = 'uuid or id'


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
