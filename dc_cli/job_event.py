import argparse
import json
import logging

from .api import AbacoAPI, DataCatalogRecord, PipelineJobEvent
from .job import JobShow, CollectionMember
from .token import get_token
from . import settings


class JobEventSend(JobShow, CollectionMember):
    """
    Send an event to a pipeline job
    """
    log = logging.getLogger(__name__)
    actor_id = settings.JOB_MANAGER_ID
    authz_nonce = settings.JOB_MANAGER_NONCE
    event_name = 'update'

    def get_parser(self, prog_name):
        parser = super(JobEventSend, self).get_parser(prog_name)
        parser.set_defaults(identifier=None)
        parser.add_argument(
            'event_name',
            choices=PipelineJobEvent.event_names(),
            nargs='?',
            help='Event name'
        )
        parser.add_argument(
            '--data',
            metavar='{data}',
            help='Event payload (JSON)'
        )
        parser.add_argument(
            '-F',
            dest='file',
            type=argparse.FileType('r'),
            help='Load event definition from file'
        )
        parser.add_argument(
            '--manager',
            dest='manager',
            metavar='<actorId>',
            default=self.actor_id,
            help='Jobs Manager actorId or actorAlias'
        )
        parser.add_argument(
            '--nonce',
            dest='nonce',
            metavar='<actorNonce>',
            default=self.authz_nonce,
            help='Jobs Manager authorization nonce'
        )
        parser.add_argument(
            '--token',
            dest='token',
            metavar='<authzToken>',
            help='Admin token'
        )
        parser.add_argument(
            '--key',
            metavar='<adminKey>',
            dest='key',
            default=settings.ADMIN_TOKEN_KEY,
            help='Key for generating an admin token'
        )
        parser.add_argument(
            '--async',
            dest='sync',
            action='store_false',
            default=True,
            help='Send event then exit'
        )
        return parser

    # This is a hacky way to amend a job record with its parent
    # pipeline.name. A better solution would rely on a server-side jobs view
    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.log.debug('Setting up client')

        tapis = AbacoAPI(api_server=self.app_args.api_server,
                         access_token=self.app_args.access_token,
                         refresh_token=self.app_args.refresh_token,
                         nonce=parsed_args.nonce)

        # read definition from file
        if parsed_args.file:
            file_event = json.load(parsed_args.file)
        else:
            file_event = dict()

        # compose from args and params
        args_event = dict()
        if parsed_args.identifier is not None:
            args_event['uuid'] = parsed_args.identifier
        if parsed_args.data:
            args_event['data'] = json.loads(parsed_args.data)

        if parsed_args.event_name is not None:
            args_event['name'] = parsed_args.event_name
        elif file_event.get('name', None) is None:
            args_event['name'] = self.event_name

        # token behavior is a little different as we can generate one
        # if none is provided
        self.log.debug('Setting authorization token')
        if parsed_args.token:
            args_event['token'] = parsed_args.token
        elif file_event.get('token', None) is not None:
            args_event['token'] = file_event.get('token')
        else:
            self.log.debug('Generating token...')
            args_event['token'] = get_token(parsed_args.key)

        # right merge favoring params
        self.log.debug('Merging event definitions...')
        event = {**file_event, **args_event}
        self.log.debug('Event: {}'.format(event))

        # Send the message to jobs-manager.prod then wait
        self.log.info('Sending "{}" to {}'.format(
            event['name'], event['uuid']))
        tapis.send_message(parsed_args.manager, event, sync=parsed_args.sync)

        # Query job and display result
        headers = self.api.get_fieldnames(self.collection)
        if 'pipeline.name' in headers:
            headers.remove('pipeline.name')
        if 'pipeline_uuid' in headers:
            headers.remove('pipeline_uuid')
        resp = self.api.get_collection_member_by_identifier(
            event['uuid'], self.collection, raw=True)
        DataCatalogRecord.set_fields(headers)
        data = DataCatalogRecord(resp).as_list()
        pipeline = self._lookup_pipeline(resp['pipeline_uuid'])
        headers.append('pipeline.name')
        data.append(pipeline.name)

        return (tuple(headers), tuple(data))
