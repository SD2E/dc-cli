import logging

from cliff.show import ShowOne
from cliff.lister import Lister
from dc_cli.api import DatabaseAPI, Verbosity
from .extended import ExtLister, ExtShowOne
from . import utils


class MongoCollectionShowOne(ShowOne):
    log = logging.getLogger(__name__)
    log.debug('Initializing MongoCollectionShowOne')
    api = None
    displayfields = None

    def take_action(self, parsed_args):

        verbosity = Verbosity.DEFAULT
        if 'return_all' in parsed_args:
            if parsed_args.return_all:
                verbosity = Verbosity.ALL
        elif 'return_identifiers' in parsed_args:
            if parsed_args.return_identifiers:
                verbosity = Verbosity.IDENTIFIERS

        self.api = DatabaseAPI(mongo_host=self.app_args.mongo_host,
                               mongo_port=self.app_args.mongo_port,
                               mongo_username=self.app_args.mongo_username,
                               mongo_password=self.app_args.mongo_password,
                               mongo_database=self.app_args.mongo_database,
                               fields=self.displayfields,
                               verbose=verbosity
                               )
        return ((), ())


class MongoCollectionLister(Lister):
    log = logging.getLogger(__name__)
    log.debug('Initializing MongoCollectionLister')
    api = None
    displayfields = None

    def take_action(self, parsed_args):
        self.log.debug(
            'MongoCollectionLister.take_action: {}'.format(parsed_args))

        verbosity = Verbosity.DEFAULT
        if 'return_all' in parsed_args:
            if parsed_args.return_all:
                verbosity = Verbosity.ALL
        elif 'return_identifiers' in parsed_args:
            if parsed_args.return_identifiers:
                verbosity = Verbosity.IDENTIFIERS

        self.api = DatabaseAPI(mongo_host=self.app_args.mongo_host,
                               mongo_port=self.app_args.mongo_port,
                               mongo_username=self.app_args.mongo_username,
                               mongo_password=self.app_args.mongo_password,
                               mongo_database=self.app_args.mongo_database,
                               fields=self.displayfields,
                               verbose=verbosity
                               )


class CollectionList(MongoCollectionLister, ExtLister):
    """List members of a specific MongoDB collection
    """
    collection = None
    pagesize = utils.env('PAGESIZE', cast=int)
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(CollectionList, self).get_parser(prog_name)

        parser.add_argument(
            '-l,'
            '--limit',
            dest='limit',
            type=int,
            help="Return first [l] records"
        )

        parser.add_argument(
            '-k',
            '--skip',
            dest='skip',
            type=int,
            help="Skip first [k] records"
        )

        parser.add_argument(
            '-p',
            '--page',
            dest='page',
            type=int,
            help="Return page [p] of {} records".format(self.pagesize)
        )

        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)

        # Pagination
        if parsed_args.page is not None:
            limit = self.pagesize
            skip = parsed_args.page * limit
        else:
            limit = parsed_args.limit
            skip = parsed_args.skip

        headers = self.api.get_fieldnames(
            self.collection, humanize=parsed_args.humanize)
        data = self.api.query_collection(
            self.collection, limit=limit, skip=skip)
        collection_members = []
        for record in data:
            collection_members.append(record)

        return (headers, tuple(collection_members))


class CollectionMember(MongoCollectionShowOne, ExtShowOne):
    """
    Get a specific record from a MongoDB collection
    """
    collection = None
    pagesize = utils.env('PAGESIZE', cast=int)
    log = logging.getLogger(__name__)
    identifier_name = '{} identifier'.format(collection)

    def get_parser(self, prog_name):
        parser = super(CollectionMember, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            type=str,
            help=self.identifier_name
        )
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)

        # Note we do not currently permit the custom field set
        data = self.api.get_collection_member_by_identifier(
            parsed_args.identifier, self.collection)
        headers = self.api.get_fieldnames(
            self.api.get_uuid_type(data[0]), humanize=parsed_args.humanize)

        return (tuple(headers), tuple(data))


class CollectionMemberFieldList(MongoCollectionLister):
    """
    Get list values from a subfield of specific MongoDb record
    """
    collection = None
    pagesize = utils.env('PAGESIZE', cast=int)
    log = logging.getLogger(__name__)
    identifier_name = '{} identifier'.format(collection)

    def get_parser(self, prog_name):
        parser = super(CollectionMemberFieldList, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            type=str,
            help=self.identifier_name
        )
        return parser
