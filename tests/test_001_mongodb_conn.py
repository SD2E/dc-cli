import os
from fixtures import *
from datacatalog import mongo

CWD = os.getcwd()
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)


def test_db_connection_settings(mongodb_settings):
    """MongoDb connection can be made with settings dict"""
    db = mongo.db_connection(mongodb_settings)
    colls = db.list_collection_names()
    assert colls is not None


def test_db_connection_authn(mongodb_authn):
    """MongoDb connection can be made with auth string"""
    db = mongo.db_connection(mongodb_authn)
    colls = db.list_collection_names()
    assert colls is not None
