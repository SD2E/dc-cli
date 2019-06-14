import argparse
import json
import logging

from .api import AbacoAPI, DataCatalogRecord, PipelineJobEvent
from .tag import TagShow, CollectionMember
from .token import get_token
from . import settings

class TagCreate(TagShow, CollectionMember):
    """
    Create a new tag
    """
    # Send a publish action to tag-manager.prod
    pass

class TagDelete(TagShow, CollectionMember):
    """
    Delete or disable a tag
    """
    # Send an unpublish action to tag-manager.prod
    pass
