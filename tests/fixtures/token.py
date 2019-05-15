import pytest
from datacatalog import tokens

__all__ = ['admin_key', 'get_admin_token']


@pytest.fixture(scope='session')
def admin_key():
    return tokens.admin.get_admin_key()


@pytest.fixture(scope='session')
def get_admin_token(admin_key):
    return tokens.admin.get_admin_token(admin_key)
