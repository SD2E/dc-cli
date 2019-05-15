import pytest
from datacatalog import mongo

__all__ = ['mongodb_localhost', 'mongodb_staging',
           'mongodb_production', 'mongodb_settings', 'mongodb_authn']


@pytest.fixture(scope='session')
def mongodb_localhost():
    settings = {'host': 'localhost', 'port': 27017,
                'username': 'catalog', 'password': 'catalog',
                'database': 'catalog_local',
                'auth_source': 'catalog_local'}
    return settings


@pytest.fixture(scope='session')
def mongodb_staging():
    settings = {'host': 'localhost', 'port': 27017,
                'username': 'catalog', 'password': 'catalog',
                'database': 'catalog_local',
                'auth_source': 'catalog_local'}
    return settings


@pytest.fixture(scope='session')
def mongodb_production():
    settings = {'host': 'localhost', 'port': 27017,
                'username': 'catalog', 'password': 'catalog',
                'database': 'catalog_local',
                'auth_source': 'catalog_local'}
    return settings


@pytest.fixture(scope='session')
def mongodb_settings(mongodb_localhost):
    settings = mongodb_localhost
    return settings


@pytest.fixture(scope='session')
def mongodb_authn(mongodb_settings):
    uri = mongo.get_mongo_uri(mongodb_settings)
    db = mongodb_settings.get('database', 'catalog_local')
    authn = mongo.encode_connection_string(uri)
    return {'authn': authn, 'database': db}
