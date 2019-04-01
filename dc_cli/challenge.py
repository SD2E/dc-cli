import logging
from .collections import CollectionList


class Challenge:
    collection = 'challenge_problem'
    displayfields = ['uuid', 'id', 'title', 'status', 'updated']


class ChallengeList(Challenge, CollectionList):
    """
    List challenge problems
    """
    log = logging.getLogger(__name__)
