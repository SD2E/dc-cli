from fixtures import *


def test_tapis_client(credentials, tapis_client):
    cl = tapis_client
    cr = credentials
    resp = cl.profiles.get()
    assert isinstance(resp, dict)
    assert cr['username'] == resp['username']
