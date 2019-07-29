import logging
from .collections import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class StructuredRequest:
    collection = 'structured_request'
    display_fields = ['uuid', 'name', 'experiment_id']
    # identifier_name = 'uuid or experiment_id'
    collection_name = 'Structured Request'
    id_fields = ['uuid']
    lst_defs = [
        ('experiment_id', 'experiment_id', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('experiment_reference_id', 'experiment_reference', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.LIKE, searchmods.NOT_LIKE,
          searchmods.IN, searchmods.NOT_IN]),
        ('challenge_problem_id', 'challenge_problem', searchtypes.STRING,
         searchmods.LIKE,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.IN, searchmods.NOT_IN,
          searchmods.LIKE, searchmods.NOT_LIKE]),
        ('experiment_version', 'experiment_version', searchtypes.INTEGER,
         searchmods.EQUALS,
         [searchmods.EQUALS, searchmods.NOT_EQUAL,
          searchmods.GREATER_THAN, searchmods.GREATER_THAN_EQUAL,
          searchmods.LESS_THAN, searchmods.LESS_THAN_EQUAL])]


class StructuredRequestList(StructuredRequest, CollectionList):
    """
    List structured requests
    """
    log = logging.getLogger(__name__)


class StructuredRequestShow(StructuredRequest, CollectionMember):
    """
    Show one structured request
    """
    log = logging.getLogger(__name__)
