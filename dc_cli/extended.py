import argparse
from cliff.lister import Lister
from cliff.show import ShowOne


class ExtShowOne(ShowOne):
    humanize = False

    def get_parser(self, prog_name):
        parser = super(ExtShowOne, self).get_parser(prog_name)
        parser.add_argument(
            '--human-ids',
            action='store_true',
            default=self.humanize,
            dest='humanize',
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            '-x', '--extended',
            action='store_true',
            dest='return_all',
            help="Return all fields"
        )
        parser.add_argument(
            '-i', '--ids',
            action='store_true',
            dest='return_identifiers',
            help="Return identifiers only"
        )
        parser.add_argument(
            '--flatten',
            action='store_true',
            dest='flatten_structs',
            help="Flatten complex field values"
        )
        return parser


class ExtLister(Lister):
    humanize = False

    def get_parser(self, prog_name):
        parser = super(ExtLister, self).get_parser(prog_name)
        parser.add_argument(
            '--human-ids',
            action='store_true',
            default=self.humanize,
            dest='humanize',
            help=argparse.SUPPRESS
        )
        parser.add_argument(
            '-x', '--extended',
            action='store_true',
            dest='return_all',
            help="Return all fields"
        )
        parser.add_argument(
            '-i', '--ids',
            action='store_true',
            dest='return_identifiers',
            help="Return identifiers only"
        )
        return parser
