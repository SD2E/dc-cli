import argparse
import json
import logging

from .api import AbacoAPI, DataCatalogRecord, PipelineJobEvent
from .text import TextShow, CollectionMember
from .token import get_token
from . import settings

class TextCreate(TextShow, CollectionMember):
    """
    Create a new text message
    """
    # Send a publish action to tag-manager.prod
    pass

class TextReply(TextShow, CollectionMember):
    """
    Reply to a text message
    """
    # Send an unpublish action to tag-manager.prod
    pass
