import argparse
import logging
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo

from . import utils

version_info = VersionInfo('dc_cli')


class CatalogApp(App):

    logger = logging.getLogger(__name__)
    if utils.env('LOGLEVEL') is not None:
        logging.basicConfig(level=utils.env('LOGLEVEL'))

    def __init__(self):
        super(CatalogApp, self).__init__(
            description='Data Catalog CLI',
            version=version_info.version_string(),
            command_manager=CommandManager('dc.cli'),
            deferred_help=True,
        )

    def build_option_parser(self, description, version):
        parser = super(CatalogApp, self).build_option_parser(
            description, version)

        parser.add_argument(
            '--mongo-host',
            metavar='HOSTNAME',
            dest='mongo_host',
            default=utils.env('MONGODB_HOST'),
            help='MongoDB hostname (Env: MONGODB_HOST)'
        )

        parser.add_argument(
            '--mongo-port',
            metavar='PORT',
            dest='mongo_port',
            default=int(utils.env('MONGODB_PORT')),
            help='MongoDB port (Env: MONGODB_PORT)'
        )

        parser.add_argument(
            '--mongo-username',
            metavar='USERNAME',
            dest='mongo_username',
            default=utils.env('MONGODB_USERNAME'),
            help='MongoDB username (Env: MONGODB_USERNAME)'
        )

        parser.add_argument(
            '--mongo-pass',
            metavar='PASSWORD',
            dest='mongo_password',
            default=utils.env('MONGODB_PASSWORD'),
            help='MongoDB password (Env: MONGODB_PASSWORD)'
        )

        parser.add_argument(
            '--mongo-database',
            metavar='DATABASE',
            dest='mongo_database',
            default=utils.env('MONGODB_DATABASE'),
            help='MongoDB database (Env: MONGODB_DATABASE)'
        )

        parser.add_argument(
            '--api-server',
            metavar='URL',
            dest='api_server',
            default=utils.env('TACC_API_SERVER'),
            help='TACC API server URL (Env: TACC_API_SERVER)'
        )

        # provide Oauth2 token via CLI
        parser.add_argument(
            '--access-token',
            metavar='ACCESS_TOKEN',
            dest='access_token',
            default=None,
            help='TACC API access token'
        )

        # hidden option - allows Tapis to refresh its Oauth session
        parser.add_argument(
            '--refresh-token',
            metavar='REFRESH_TOKEN',
            dest='refresh_token',
            help=argparse.SUPPRESS
        )

        # TODO: Options to manage MongoDB TLS, Tapis cert validation
        return parser

    def initialize_app(self, argv):
        super(CatalogApp, self).initialize_app(argv)
        self.logger.debug('Starting app, options: {}'.format(self.options))


def main(argv=sys.argv[1:]):
    catalogApp = CatalogApp()
    return catalogApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
