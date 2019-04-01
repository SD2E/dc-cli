import logging
from cliff.show import ShowOne
from dc_cli.api import DatabaseAPI, Verbosity
from . import utils


class Member(ShowOne):
    collection = None
    displayfields = None
    pagesize = 1
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Member, self).get_parser(prog_name)

        parser.add_argument('identifier', help='A valid identifier')

        parser.add_argument(
            '-x, --extended',
            action='store_true',
            dest='return_all',
            help="Return all fields"
        )

        parser.add_argument(
            '-i, --ids',
            action='store_true',
            dest='return_identifiers',
            help="Return identifiers only"
        )

        # parser.add_argument(
        #     '-t, --type',
        #     action='store_true',
        #     dest='return_type',
        #     help="Return identifier type only"
        # )

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
                          fields=self.displayfields,
                          verbose=verbosity
                          )

        headers = api.get_fieldnames(
            self.collection)
        data = api.query_collection(
            self.collection, limit=1, skip=0)
        collection_members = []
        for record in data:
            collection_members.append(record)

        return (headers, tuple(collection_members))
