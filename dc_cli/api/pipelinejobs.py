from attrdict import AttrDict
from datacatalog.linkedstores.pipelinejob.fsm import JobStateMachine
from datacatalog.identifiers import typeduuid
from datacatalog.tokens import Token


class PipelineJobEvent(AttrDict):
    """Simple container and validator class for a PipelineJob Event
    """
    # param name, mandatory?, attr_name, default
    PARAMS = [('uuid', True, 'uuid', None),
              ('name', True, 'name', None),
              ('data', True, 'data', {}),
              ('token', False, 'token', None)]

    def __init__(self, **kwargs):
        for param, mandatory, attr, default in self.PARAMS:
            try:
                value = (kwargs[param] if mandatory
                         else kwargs.get(param, default))
            except KeyError:
                pass
            setattr(self, attr, value)

        # validate UUID
        assert typeduuid.get_uuidtype(self.uuid) == 'pipelinejob'
        # validate name
        assert self.name in JobStateMachine.get_events()
        # validate data is dict
        assert isinstance(self.data, dict)
        self.token = Token(self.token)
