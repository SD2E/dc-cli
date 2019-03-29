import logging
from cliff.show import ShowOne
from datacatalog.tokens import get_admin_token, get_admin_lifetime


class TokenShow(ShowOne):
    """
    Fetch the current administrative token
    """

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(TokenShow, self).get_parser(prog_name)
        parser.add_argument('key', help='the admin token key')
        return parser

    def take_action(self, parsed_args):
        column_headers = ('token', 'expires')
        token = get_admin_token(parsed_args.key)
        expires = get_admin_lifetime()
        record = (token, expires)
        return (column_headers, record)
