from agavepy.agave import Agave, AgaveError
import logging
import bacanora
from .constants import (MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE,
                        MONGODB_USERNAME, MONGODB_PASSWORD,
                        API_SERVER, PAGESIZE)


class Verbosity:
    QUIET = 0
    VERBOSE = 1
    VERYVERBOSE = 2
    DEFAULT = QUIET


class AgaveAPI(object):
    """Main class for accessing Tapis APIs

    Args:
        verbose (bool): Whether to return complete or summary responses
    """

    log = logging.getLogger(__name__)
    client = None

    def __init__(self, api_server=API_SERVER,
                 api_token=None,
                 refresh_token=None,
                 verbose=Verbosity.DEFAULT):

        # TODO - Implement refresh_token
        try:
            if api_token is not None:
                self.log.debug('Using supplied Tapis credentials')
                ag = Agave(api_server=api_server, token=api_token)
            else:
                # Use local credential cache
                self.log.debug('Laoding from local Tapis credential cache')
                ag = Agave.restore()
        except Exception:
            self.log.exception('Unable to initialize Tapis client')
            raise

        self.client = ag
        self.verbosity = verbose
