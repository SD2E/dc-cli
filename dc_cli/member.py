import logging
from cliff.show import ShowOne
from dc_cli.api import DatabaseAPI, Verbosity


class MemberShow(ShowOne):
    collection = None
    display_fields = None
    pagesize = 1
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(MemberShow, self).get_parser(prog_name)

        parser.add_argument('identifier', help='A valid identifier')

        parser.add_argument(
            '-x', '--extended',
            action='store_true',
            dest='return_all',
            help="Return all fields"
        )

        parser.add_argument(
            '-i', '--ids',
            action='store_true',
            dest='return_identifiers',
            help="Return identifiers only"
        )

        return parser

    def take_action(self, parsed_args):

        # Response verbosity
        verbosity = Verbosity.DEFAULT
        if parsed_args.return_all:
            verbosity = Verbosity.ALL
        elif parsed_args.return_identifiers:
            verbosity = Verbosity.IDENTIFIERS

        api = DatabaseAPI(mongo_host=self.app_args.mongo_host,
                          mongo_port=self.app_args.mongo_port,
                          mongo_username=self.app_args.mongo_username,
                          mongo_password=self.app_args.mongo_password,
                          mongo_database=self.app_args.mongo_database,
                          fields=self.display_fields,
                          verbose=verbosity
                          )

        headers = api.get_fieldnames(
            self.collection)
        data = api.get_by_identifier(parsed_args.id)
        return (headers, data)
