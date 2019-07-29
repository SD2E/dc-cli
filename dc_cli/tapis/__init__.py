import argparse
from agavepy.agave import AgaveError as TapisError
from cliff.lister import Lister
from cliff.show import ShowOne
from ..api.agave import AgaveAPI

__all__ = ['TapisShowOne', 'TapisLister', 'TapisError']


class TapisManager(object):
    def __init__(self):
        self.log.debug('Init Tapis Manager')
        self.tapis = AgaveAPI(api_server=self.app_args.api_server,
                              token=self.app_args.access_token,
                              refresh_token=self.app_args.refresh_token)


class TapisShowOne(TapisManager, ShowOne):
    pass


class TapisLister(TapisManager, Lister):
    pass
