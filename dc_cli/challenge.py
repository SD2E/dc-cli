import logging
from .collections import (CollectionList, CollectionMember, searchmods)


class Challenge:
    collection = 'challenge_problem'
    collection_name = 'Challenge Problem'
    display_fields = ['uuid', 'id', 'title', 'status', 'updated']
    id_fields = ['uuid', 'id']
    lst_defs = [('status', 'status', searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN]),
                ('title', 'title', searchmods.LIKE,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.LIKE, searchmods.NOT_LIKE,
                  searchmods.IN, searchmods.NOT_IN]),
                ('id', 'id', searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN,
                  searchmods.LIKE, searchmods.NOT_LIKE])]


class ChallengeList(Challenge, CollectionList):
    """
    List challenge problems
    """
    log = logging.getLogger(__name__)


class ChallengeShow(Challenge, CollectionMember):
    """
    Get one challenge problem
    """
    log = logging.getLogger(__name__)
