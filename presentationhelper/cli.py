#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

import sys

from argparse import ArgumentParser


COMMAND = 'presentation-helper'

OPTIONS = """
options:
  - 'flags': ['-v', '--verbose']
    action: count
    help: 'verbose output (repeat for more verbosity)'
    dest: verbosity
    default: 0
  - 'flags': ['-q', '--quiet']
    action: store_const
    help: 'quiet output (show errors only)'
    const: -1
    dest: verbosity
subcommands:
- create:
    options:
      - 'flags': ['-F', '--flavor']
        'choices': ['reveal']
        'help': 'Presentation flavor'
        'default': 'reveal'
        dest: flavor
      - 'flags': ['-c', '--config']
        'help': 'YAML configuration file'
        dest: config
"""


def walk_opts(dictionary, parser):
    """Walk a dictionary and populate an ArgumentParser."""

    if 'options' in dictionary:
        for opt in dictionary['options']:
            args = ()
            try:
                args = opt.pop('flags')
            except KeyError:
                # item has no 'flags' key, represents a positional
                # argument
                pass
            kwargs = opt
            parser.add_argument(*args,
                                **kwargs)

    if 'subcommands' in dictionary:
        subs = parser.add_subparsers(dest='action')
        for subcommand in dictionary['subcommands']:
            for cmd, opts in subcommand.items():
                sub = subs.add_parser(cmd)
                walk_opts(opts, sub)


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
        walk_opts(options, parser)

        self.parser = parser

    def create(self, args):
        if args.flavor == 'reveal':
            from .reveal import RevealPresentationCreator as Creator

        creator = Creator(config_path=args.config)

        creator.create()

    def main(self, argv=sys.argv):
        args = self.parser.parse_args(argv[1:])

        if args.action:
            getattr(self, args.action)(args)


def main(argv=sys.argv):
    CLI().main(argv)
