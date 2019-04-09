from agavepy.agave import Agave, AgaveError
import logging
import bacanora
from .. import utils
from .constants import (MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE,
                        MONGODB_USERNAME, MONGODB_PASSWORD,
                        API_SERVER, PAGESIZE, STORAGE_SYSTEM,
                        REACTOR_MESSAGE_SYNC)


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
                 access_token=None,
                 refresh_token=None,
                 verbose=Verbosity.DEFAULT):
        self.log.debug('Initialize Agave API client')
        # TODO - Implement refresh_token
        try:
            if access_token is not None:
                self.log.debug('Using supplied Tapis credentials')
                ag = Agave(api_server=api_server, token=access_token)
            else:
                # Use local credential cache
                self.log.debug('Laoding from local Tapis credential cache')
                ag = Agave.restore()
        except Exception:
            self.log.exception('Unable to initialize Tapis client')
            raise

        self.client = ag
        self.verbosity = verbose

    def download(self, file_to_download, local_filename=None,
                 system_id=STORAGE_SYSTEM):
        return bacanora.download(self.client,
                                 file_to_download,
                                 local_filename=local_filename,
                                 system_id=system_id)

    def to_agave_uri(self, system_id, dir_path):
        return bacanora.agaveutils.to_agave_uri(system_id, dir_path)


class AbacoAPI(object):
    log = logging.getLogger(__name__)
    client = None
    sync = REACTOR_MESSAGE_SYNC

    def __init__(self,
                 api_server=API_SERVER,
                 nonce=None,
                 access_token=None,
                 refresh_token=None,
                 sync=REACTOR_MESSAGE_SYNC,
                 verbose=Verbosity.DEFAULT):
        self.log.debug('Initialize Abaco API client')
        try:
            if nonce is not None:
                self.log.debug('Using Abaco authorization nonce')
                ag = bacanora.agaveutils.AgaveNonceOnly(
                    api_server=api_server, nonce=nonce)
            elif access_token is not None:
                self.log.debug('Using supplied Tapis credentials')
                ag = Agave(api_server=api_server, token=access_token)
            else:
                # Use local credential cache
                self.log.debug('Using local Tapis credential cache')
                ag = Agave.restore()
        except Exception:
            self.log.exception('Unable to initialize Tapis client')
            raise

        self.log.debug('Done initializing Abaco API client')
        self.client = ag
        self.sync = sync
        self.verbosity = verbose

    def send_message(self, actor_id, message, sync=True, **kwargs):
        return bacanora.agaveutils.send_message(self.client,
                                                actor_id,
                                                message,
                                                sync=self.sync,
                                                **kwargs)

    def await_actor_execution(self, actor_id, execution_id, **kwargs):
        return bacanora.agaveutils.await_actor_execution(self.client,
                                                         actorId=actor_id,
                                                         executionId=execution_id,
                                                         **kwargs)
