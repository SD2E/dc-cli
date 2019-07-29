import logging
from ..api import DatabaseAPI, Verbosity
from ..extended import ExtShowOne


class IdentifiedRecord:
    pass


class IdentifiedRecordShow(IdentifiedRecord, ExtShowOne):
    """
    Get a record by one of its identifiers
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(IdentifiedRecordShow, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            type=str,
            help='Data Catalog identifier'
        )
        parser.add_argument(
            'field',
            type=str,
            default=None,
            nargs='?',
            help='Field from record (optional)'
        )
        return parser

    def take_action(self, parsed_args):

        # Response verbosity
        # Note we do not currently permit the custom field set
        verbosity = Verbosity.IDENTIFIERS
        if parsed_args.return_all:
            verbosity = Verbosity.ALL
        elif parsed_args.return_identifiers:
            verbosity = Verbosity.IDENTIFIERS

        api = DatabaseAPI(mongo_host=self.app_args.mongo_host,
                          mongo_port=self.app_args.mongo_port,
                          mongo_username=self.app_args.mongo_username,
                          mongo_password=self.app_args.mongo_password,
                          mongo_database=self.app_args.mongo_database,
                          verbose=verbosity,
                          flatten=parsed_args.flatten_structs
                          )

        data = api.get_by_identifier(parsed_args.identifier)
        headers = api.get_fieldnames(
            api.get_uuid_type(data[0]), humanize=parsed_args.humanize)

        return (tuple(headers), tuple(data))
