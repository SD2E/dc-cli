import logging
from cliff.command import Command

VERSION = '0.1.0'


class Version(Command):
    """Show Data Catalog schema and code version."""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.app.stdout.write('Versions:')
        self.app.stdout.write('    dc_cli: ' + VERSION)
