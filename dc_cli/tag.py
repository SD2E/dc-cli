import logging
from .collections import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class TagAnno:
    collection = 'tag_annotation'
    collection_name = 'Keyword Tag'
    display_fields = ['uuid', 'name', 'owner']
    id_fields = ['uuid']
    lst_defs = [
                ('owner', 'owner', searchtypes.STRING,
                 searchmods.LIKE,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.LIKE, searchmods.NOT_LIKE,
                  searchmods.IN, searchmods.NOT_IN]),
                ('name', 'name', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN,
                  searchmods.LIKE, searchmods.NOT_LIKE])]


class TagList(TagAnno, CollectionList):
    """
    List tags
    """
    log = logging.getLogger(__name__)


class TagShow(TagAnno, CollectionMember):
    """
    Get one tag
    """
    log = logging.getLogger(__name__)
