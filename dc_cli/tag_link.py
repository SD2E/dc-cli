import argparse
import json
import logging

from .api import AbacoAPI, DataCatalogRecord, PipelineJobEvent
from .tag import TagShow, CollectionMember
from .token import get_token
from . import settings

class TagLink(TagShow, CollectionMember):
    """
    Link an existing tag to a Data Catalog record
    """
    # Send a publish action to tag-manager.prod
    pass

class TagUnlink(TagShow, CollectionMember):
    """
    Unlink a tag from a Data Catalog record
    """
    pass
