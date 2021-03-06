import os
import logging
from cliff.show import ShowOne
from datacatalog.tokens import get_admin_token, get_admin_lifetime
from . import settings


class TokenGenerate(ShowOne):
    """
    Generate an administrative token for managing Data Catalog records
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TokenGenerate, self).get_parser(prog_name)
        parser.add_argument(
            '--key',
            metavar='<adminKey>',
            dest='key',
            default=settings.ADMIN_TOKEN_KEY,
            help='Key for generating an admin token'
        )
        return parser

    def take_action(self, parsed_args):
        column_headers = ('token', 'expires')
        token = get_token(parsed_args.key)
        expires = get_admin_lifetime()
        record = (token, expires)
        return (column_headers, record)


def get_token(key):
    os.environ['CATALOG_ADMIN_TOKEN_KEY'] = key
    return get_admin_token(key)
