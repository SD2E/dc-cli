import bacanora
import logging
from cliff.show import ShowOne
from .api import DatabaseAPI, Verbosity, AgaveAPI, AgaveError
from .collections import (MongoCollectionShowOne,
                          CollectionList, CollectionMember)
from . import settings


class File:
    collection = 'file'
    collection_name = 'File'
    id_fields = ['uuid', 'file_id', 'name']


class FileList(File, CollectionList):
    """
    List managed files
    """
    log = logging.getLogger(__name__)


class FileShow(File, CollectionMember):
    """
    Show one file by identifier
    """
    log = logging.getLogger(__name__)
    log.debug('Init FileShow')


class FileGet(File, MongoCollectionShowOne):
    """
    Download a file by identifier
    """
    log = logging.getLogger(__name__)
    log.debug('Init FileGet')

    def get_parser(self, prog_name):
        id_display_name = '{} {}'.format(
            self.collection_name, self.humanized_id_fields())
        parser = super(MongoCollectionShowOne, self).get_parser(prog_name)
        parser.add_argument(
            'identifier',
            type=str,
            help=id_display_name
        )
        parser.add_argument(
            '-O',
            dest='output',
            default=None,
            help='Destination filename'
        )
        return parser

    def take_action(self, parsed_args):

        tapis = AgaveAPI(api_server=self.app_args.api_server,
                         access_token=self.app_args.access_token,
                         refresh_token=self.app_args.refresh_token)

        verbosity = Verbosity.DEFAULT
        api = DatabaseAPI(mongo_host=self.app_args.mongo_host,
                          mongo_port=self.app_args.mongo_port,
                          mongo_username=self.app_args.mongo_username,
                          mongo_password=self.app_args.mongo_password,
                          mongo_database=self.app_args.mongo_database,
                          fields=self.display_fields,
                          verbose=verbosity)

        # Note we do not currently permit the custom field set
        data = api.get_collection_member_by_identifier(
            parsed_args.identifier, self.collection, raw=True)

        system_id = data.get(
            'storage_system', settings.TACC_PRIMARY_STORAGE_SYSTEM)

        resp = tapis.download(data['name'], parsed_args.output,
                              system_id=system_id)

        if resp is not None:
            headers = ('uri', 'destination')
            uri = bacanora.agaveutils.to_agave_uri(system_id, data['name'])
            data = (uri, resp)

        return (headers, data)
