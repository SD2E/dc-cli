import argparse
from cliff.lister import Lister
from cliff.show import ShowOne
from .api.agave import AgaveAPI
from agavepy.agave import AgaveError as TapisError

__all__ = ['TapisShowOne', 'TapisLister', 'TapisError']


class TapisManager(AgaveAPI):
    def __init__(self):
        super(TapisManager, self).__init__(api_server=self.app_args.api_server,
                                           token=self.app_args.access_token,
                                           refresh_token=self.app_args.refresh_token)


class TapisShowOne(TapisManager, ShowOne):
    pass


class TapisLister(TapisManager, Lister):
    pass
