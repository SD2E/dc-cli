import logging

from dc_cli.api import DatabaseAPI, Verbosity
from .extended import ExtLister
from . import utils


class CollectionList(ExtLister):
    collection = None
    displayfields = None
    pagesize = int(utils.env('CATALOG_PAGESIZE'))
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CollectionList, self).get_parser(prog_name)

        parser.add_argument(
            '-l, --limit',
            dest='limit',
            help="Return first [l] records"
        )

        parser.add_argument(
            '-k, --skip',
            dest='skip',
            help="Skip first [k] records"
        )

        parser.add_argument(
            '-p, --page',
            dest='page',
            help="Return page [p] of {} records".format(self.pagesize)
        )

        # parser.add_argument(
        #     '-x, --extended',
        #     action='store_true',
        #     dest='return_all',
        #     help="Return all fields"
        # )

        # parser.add_argument(
        #     '-i, --ids',
        #     action='store_true',
        #     dest='return_identifiers',
        #     help="Return identifiers only"
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

        # Pagination
        if parsed_args.page is not None:
            limit = self.pagesize
            skip = parsed_args.page * limit
        else:
            limit = parsed_args.limit
            skip = parsed_args.skip

        headers = api.get_fieldnames(
            self.collection, humanize=parsed_args.humanize)
        data = api.query_collection(
            self.collection, limit=limit, skip=skip)
        collection_members = []
        for record in data:
            collection_members.append(record)

        return (headers, tuple(collection_members))
