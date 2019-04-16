import logging
from .collections import (
    CollectionList, CollectionMember, CollectionMemberFieldList,
    searchmods, searchtypes)
from .api import DataCatalogRecord
from .pipeline import PipelineRecord


class Job:
    collection = 'pipelinejob'
    collection_name = 'Pipeline Job'
    display_fields = ['uuid', 'state', 'updated']
    id_fields = ['uuid']
    lst_defs = [('state', 'state', searchtypes.STRING,
                 searchmods.EQUALS,
                 [searchmods.EQUALS, searchmods.NOT_EQUAL,
                  searchmods.IN, searchmods.NOT_IN])]

    def _lookup_pipeline(self, pipeline_uuid):
        resp = self.api.get_collection_member_by_identifier(
            pipeline_uuid, collection='pipeline', raw=True)
        return PipelineRecord(resp['uuid'], resp['name'], resp['id'])


class JobList(Job, CollectionList):
    """
    List pipeline jobs
    """
    log = logging.getLogger(__name__)

    # TODO - the inelegance has come back to bite me as the 2x database query breaks filtering

    # This is a hacky way to amend a job record with its parent
    # pipeline.name. A better solution would rely on a server-side jobs view
    def take_action(self, parsed_args):
        super().take_action(parsed_args)

        # Pagination
        if parsed_args.page is not None:
            limit = self.pagesize
            skip = parsed_args.page * limit
        else:
            limit = parsed_args.limit
            skip = parsed_args.skip

        headers = self.api.get_fieldnames(self.collection)
        if 'pipeline_uuid' not in headers:
            headers.append('pipeline_uuid')
        data = self.api.query_collection(
            self.collection, limit=limit, skip=skip)
        collection_members = []
        for record in data:
            pipeline_uuid = record[len(record) - 1]
            pipeline = self._lookup_pipeline(pipeline_uuid)
            record.remove(pipeline_uuid)
            record.append(pipeline.name)
            collection_members.append(record)
        if 'pipeline_uuid' in headers:
            headers.remove('pipeline_uuid')
            headers.append('pipeline.name')
        return (headers, tuple(collection_members))


class JobShow(Job, CollectionMember):
    """
    Show one pipeline job
    """
    log = logging.getLogger(__name__)

    # This is a hacky way to amend a job record with its parent
    # pipeline.name. A better solution would rely on a server-side jobs view
    def take_action(self, parsed_args):
        super().take_action(parsed_args)

        headers = self.api.get_fieldnames(self.collection)
        if 'pipeline_uuid' in headers:
            headers.remove('pipeline_uuid')
        resp = self.api.get_collection_member_by_identifier(
            parsed_args.identifier, self.collection, raw=True)
        DataCatalogRecord.set_fields(headers)
        data = DataCatalogRecord(resp).as_list()

        pipeline = self._lookup_pipeline(resp['pipeline_uuid'])
        headers.append('pipeline.name')
        data.append(pipeline.name)

        return (tuple(headers), tuple(data))


class JobHistoryShow(Job, CollectionMemberFieldList):
    """Show a pipeline job's event history"""

    def take_action(self, parsed_args):

        super().take_action(parsed_args)
        headers = ['uuid', 'date', 'name']
        resp = self.api.get_collection_member_by_identifier(
            parsed_args.identifier, self.collection, raw=True)

        resp_history = resp.get('history')
        history = list()
        DataCatalogRecord.set_fields(headers)
        for hst in resp_history:
            history.append(DataCatalogRecord(hst).as_list())

        return (headers, tuple(history))
