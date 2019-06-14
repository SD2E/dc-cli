import argparse
import json
import logging

from .api import AbacoAPI, DataCatalogRecord, PipelineJobEvent
from .tag import TagShow, CollectionMember
from .token import get_token
from . import settings

class TagPublish(TagShow, CollectionMember):
    """
    Clone a private tag into the public namespace
    """
    # Send a publish action to tag-manager.prod
    pass

class TagUnpublish(TagShow, CollectionMember):
    """
    Remove a tag from the public namespace
    """
    # Send an unpublish action to tag-manager.prod
    pass
