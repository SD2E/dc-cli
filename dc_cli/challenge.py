import logging
from .collections import CollectionList


class ChallengeList(CollectionList):
    collection = 'challenge_problem'
    log = logging.getLogger(__name__)
