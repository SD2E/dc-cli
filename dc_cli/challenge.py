import logging
from .collections import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class Challenge:
    collection = 'challenge_problem'
    collection_name = 'Challenge Problem'
    display_fields = ['uuid', 'id', 'title', 'status', 'updated']
    id_fields = ['uuid', 'id']
    lst_defs = [('status', 'status', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN]),
                ('title', 'title', searchtypes.STRING,
                 searchmods.LIKE,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.LIKE, searchmods.NOT_LIKE,
                  searchmods.IN, searchmods.NOT_IN]),
                ('id', 'id', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN,
                  searchmods.LIKE, searchmods.NOT_LIKE]),
                ('created', 'created', searchtypes.DATETIME,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.GREATER_THAN, searchmods.GREATER_THAN_EQUAL,
                  searchmods.LESS_THAN, searchmods.LESS_THAN_EQUAL]),
                ('updated', 'updated', searchtypes.DATETIME,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.GREATER_THAN, searchmods.GREATER_THAN_EQUAL,
                  searchmods.LESS_THAN, searchmods.LESS_THAN_EQUAL])]


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
