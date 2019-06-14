import logging
from .collections import (
    CollectionList, CollectionMember, searchmods, searchtypes)


class TextAnno:
    collection = 'text_annotation'
    collection_name = 'Text Message'
    display_fields = ['uuid', 'owner', 'subject', 'body']
    id_fields = ['uuid']
    lst_defs = [
                ('owner', 'owner', searchtypes.STRING,
                 searchmods.LIKE,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.LIKE, searchmods.NOT_LIKE,
                  searchmods.IN, searchmods.NOT_IN]),
                ('subject', 'subject', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN,
                  searchmods.LIKE, searchmods.NOT_LIKE])]


class TextList(TextAnno, CollectionList):
    """
    List text messages
    """
    log = logging.getLogger(__name__)


class TextShow(TextAnno, CollectionMember):
    """
    Get one text message
    """
    log = logging.getLogger(__name__)

# TODO - Can we implement some kind of threaded view?
