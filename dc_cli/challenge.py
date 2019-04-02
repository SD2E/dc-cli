import logging
from .collections import CollectionList
from .member import MemberShow


class Challenge:
    collection = 'challenge_problem'
    displayfields = ['uuid', 'id', 'title', 'status', 'updated']


class ChallengeList(Challenge, CollectionList):
    """
    List challenge problems
    """
    log = logging.getLogger(__name__)


class ChallengeShow(Challenge, MemberShow):
    """
    Show one challenge problems
    """
    log = logging.getLogger(__name__)
