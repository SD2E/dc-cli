import logging
from .collections import CollectionList


class Challenge:
    collection = 'challenge_problem'


class ChallengeList(Challenge, CollectionList):
    """
    List challenge problems
    """
    log = logging.getLogger(__name__)
