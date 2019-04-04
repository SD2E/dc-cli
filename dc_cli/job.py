import logging
from .collections import CollectionList, CollectionMember
from .api import DataCatalogRecord
from .pipeline import PipelineRecord


class Job:
    collection = 'pipelinejob'
    displayfields = ['uuid', 'state', 'updated']

    def _lookup_pipeline(self, pipeline_uuid):
        resp = self.api.get_collection_member_by_identifier(
            pipeline_uuid, collection='pipeline', raw=True)
        return PipelineRecord(resp['uuid'], resp['name'], resp['id'])


class JobList(Job, CollectionList):
    """
    List pipeline jobs
    """
    log = logging.getLogger(__name__)

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
