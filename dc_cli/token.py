import os
import logging
from cliff.show import ShowOne
from datacatalog.tokens import get_admin_token, get_admin_lifetime
from . import utils


class TokenShow(ShowOne):
    """
    Get an administrative token
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TokenShow, self).get_parser(prog_name)
        parser.add_argument(
            '--key',
            metavar='<admin-key>',
            dest='key',
            default=utils.env('ADMIN_TOKEN_KEY'),
            help='Admin token key (Env: ADMIN_TOKEN_KEY)'
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
