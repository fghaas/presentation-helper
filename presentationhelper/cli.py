import yaml

import sys

from argparse import ArgumentParser


COMMAND = 'presentation-helper'

OPTIONS = """
create:
  - 'flags': ['-F', '--flavor']
    'choices': ['reveal', 'generic']
    'help': 'Presentation flavor'
    'default': 'generic'
  - 'flags': ['-t', '--template']
    'help': 'Jinja2 template file'
  - 'flags': ['-c', '--config']
    'help': 'YAML configuration file'
  - 'flags': ['-o', '--output']
    'help': 'Output file'
"""


class CLI(object):
    """presentation-helper command-line interface.

    Understands the following sub-commands:

    create - Create a new presentation
    """

    def __init__(self):
        self.setup_argparse()

    def setup_argparse(self):
        options = yaml.safe_load(OPTIONS)

        parser = ArgumentParser(description=self.__doc__)
        sub = parser.add_subparsers(dest='action')

        for cmd, opts in options.items():
            subparser = sub.add_parser(cmd)
            for opt in opts:
                args = opt.pop('flags')
                kwargs = opt
                subparser.add_argument(*args,
                                       **kwargs)

        self.parser = parser

    def create(self, args):
        if args.flavor == 'generic':
            from .generic import PresentationCreator as Creator
        elif args.flavor == 'reveal':
            from .reveal import RevealPresentationCreator as Creator

        creator = Creator(config_path=args.config,
                          template_path=args.template,
                          output_path=args.output)

        creator.create()

    def main(self, argv=sys.argv):
        args = self.parser.parse_args(argv[1:])

        if args.action:
            getattr(self, args.action)(args)


def main(argv=sys.argv):
    CLI().main(argv)
