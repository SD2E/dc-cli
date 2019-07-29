import logging

from cliff.show import ShowOne
from cliff.lister import Lister
from ..api import (DatabaseAPI, Verbosity)
from ..extended import (ExtLister, ExtShowOne)
from ..search import (SearchArg, searchmods, searchtypes)
from . import settings

__all__ = ['MongoCollectionShowOne', 'MongoCollectionLister',
           'CollectionList', 'CollectionMemberFieldList']


class CollectionBase:
    api = None
    log = logging.getLogger(__name__)
    collection = None
    collection_name = None
    display_fields = None
    id_fields = None
    pagesize = settings.PAGESIZE
    lst_defs = list()
    search_args = dict()

    @classmethod
    def humanized_id_fields(cls):
        if cls.id_fields is not None:
            return ', '.join(cls.id_fields[0:-1]) + ' or ' + cls.id_fields[-1]


class MongoCollectionShowOne(CollectionBase, ShowOne):

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
                               fields=self.display_fields,
                               verbose=verbosity
                               )
        return ((), ())


class MongoCollectionLister(CollectionBase, Lister):

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
                               fields=self.display_fields,
                               verbose=verbosity
                               )


class CollectionList(MongoCollectionLister, ExtLister):
    """List members of a specific MongoDB collection
    """

    def get_parser(self, prog_name):
        parser = super(CollectionList, self).get_parser(prog_name)

        parser.add_argument(
            '--limit',
            dest='limit',
            type=int,
            help="Return first [l] records"
        )

        parser.add_argument(
            '--skip',
            dest='skip',
            type=int,
            help="Skip first [k] records"
        )

        parser.add_argument(
            '--page',
            dest='page',
            type=int,
            help="Return page [p] of {} records".format(self.pagesize)
        )

        # These are custom filter arguments
        # TODO Add `type`
        for arg, field, field_type, def_mod, mods in self.lst_defs:
            sarg = SearchArg(argument=arg, field=field,
                             default_mod=def_mod, mods=mods,
                             field_type=field_type)
            sargp = sarg.argparse()
            self.search_args[arg] = sarg
            parser.add_argument(sargp.argument,
                                **sargp.attributes)

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

        # Build up filters
        filters = list()
        for sa, sv in self.search_args.items():
            if getattr(parsed_args, sa):
                arg_qval = sv.get_query(getattr(parsed_args, sa))
                filters.append(arg_qval)
        if len(filters) > 0:
            filt = {'$and': filters}
        else:
            # Allow for no filters (duh!)
            filt = {}

        headers = self.api.get_fieldnames(
            self.collection, humanize=parsed_args.humanize)
        data = self.api.query_collection(
            self.collection, filter=filt, limit=limit, skip=skip)
        collection_members = []
        for record in data:
            collection_members.append(record)

        self.log.info('CollectionList.take_action complete: {}'.format(
            len(collection_members)))
        return (headers, tuple(collection_members))


class CollectionMember(MongoCollectionShowOne, ExtShowOne):
    """
    Get a specific record from a MongoDB collection
    """

    def get_parser(self, prog_name):
        id_display_name = '{} {}'.format(
            self.collection_name, self.humanized_id_fields())
        parser = super(CollectionMember, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            type=str,
            help=id_display_name
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

    def get_parser(self, prog_name):
        id_display_name = '{} {}'.format(
            self.collection_name, self.humanized_id_fields())
        parser = super(CollectionMemberFieldList, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            type=str,
            help=id_display_name
        )
        return parser
