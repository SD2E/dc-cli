import sys
import argparse
import logging

from cliff.app import App
from cliff.commandmanager import CommandManager
from pbr.version import VersionInfo

from . import utils

version_info = VersionInfo('dc_cli')


class CatalogApp(App):

    logger = logging.getLogger(__name__)

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
            metavar='<mongo-host>',
            dest='mongo_host',
            default=utils.env('MONGODB_HOST'),
            help='MongoDB host (Env: MONGODB_HOST)'
        )

        parser.add_argument(
            '--mongo-port',
            metavar='<mongo-port>',
            dest='mongo_port',
            default=int(utils.env('MONGODB_PORT')),
            help='MongoDB port (Env: MONGODB_PORT)'
        )

        parser.add_argument(
            '--mongo-username',
            metavar='<mongo-username>',
            dest='mongo_username',
            default=utils.env('MONGODB_USERNAME'),
            help='MongoDB port (Env: MONGODB_USERNAME)'
        )

        parser.add_argument(
            '--mongo-pass',
            metavar='<mongo-pass>',
            dest='mongo_password',
            default=utils.env('MONGODB_PASSWORD'),
            help='MongoDB port (Env: MONGODB_PASSWORD)'
        )

        parser.add_argument(
            '--mongo-database',
            metavar='<mongo-database>',
            dest='mongo_database',
            default=utils.env('MONGODB_DATABASE'),
            help='MongoDB port (Env: MONGODB_DATABASE)'
        )
        # provide Oauth2 token via CLI
        parser.add_argument(
            '--tacc-acess-token',
            metavar='<tacc-access-token>',
            dest='tacc_access_token',
            default=utils.env('ACCESS_TOKEN'),
            help='TACC API access token (Env: ACCESS_TOKEN)'
        )

        parser.add_argument(
            '--tacc-api-server',
            metavar='<tacc-api-server>',
            dest='tacc_api_server',
            default=utils.env('API_SERVER'),
            help='TACC API server URL (Env: API_SERVER)'
        )

        return parser

    def initialize_app(self, argv):
        super(CatalogApp, self).initialize_app(argv)
        self.logger.debug('Starting app, options: {}'.format(self.options))


def main(argv=sys.argv[1:]):
    catalogApp = CatalogApp()
    return catalogApp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
