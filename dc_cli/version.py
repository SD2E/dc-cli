import logging
from cliff.command import Command
from datacatalog.version import __version__ as dc_version
from . import settings

VERSION = '0.1.0'


class Version(Command):
    """Show Data Catalog schema and code version."""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.app.stdout.write('Versions:')
        self.app.stdout.write('    dcat: ' + VERSION)
        self.app.stdout.write('    python-datacatalog: ' + dc_version)
        self.app.stdout.write('    jsonschema: ' + 'Unknown')
        self.app.stdout.write('    mongodb.database: ' +
                              settings.MONGODB_DATABASE)
