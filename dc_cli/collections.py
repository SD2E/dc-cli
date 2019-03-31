import logging

from cliff.lister import Lister
from cliff.show import ShowOne
from dc_cli.api import DatabaseAPI


class CollectionList(Lister):
    collection = None
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CollectionList, self).get_parser(prog_name)
        parser.add_argument(
            '-x, --extended',
            action='store_true',
            dest='extended',
            help="Return all fields"
        )
        return parser

    def take_action(self, parsed_args):
        api = DatabaseAPI(mongo_host=self.app_args.mongo_host,
                          mongo_port=self.app_args.mongo_port,
                          mongo_username=self.app_args.mongo_username,
                          mongo_password=self.app_args.mongo_password,
                          mongo_database=self.app_args.mongo_database,
                          verbose=parsed_args.extended
                          )

        headers = api.get_fieldnames(
            self.collection)
        data = api.query_collection(
            self.collection)
        collection_members = []
        for record in data:
            collection_members.append(record)

        return (headers, tuple(collection_members))
