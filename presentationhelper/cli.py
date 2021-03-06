#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
from argparse import ArgumentParser

import yaml

from . import __version__


COMMAND = 'presentation-helper'

VERSION = '%(prog)s ' + __version__

OPTIONS = """
options:
  - 'flags': ['-V', '--version']
    action: version
    help: 'show version'
    version: '%s'
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
  - 'flags': ['-F', '--flavor']
    'choices': ['reveal']
    'help': 'Presentation flavor'
    'default': 'reveal'
    dest: flavor
subcommands:
- create:
    options:
      - 'flags': ['-c', '--config']
        'help': 'YAML configuration file'
        dest: config
- 'default-config':
    options:
      - 'flags': ['-o', '--output']
        'help': 'output file'
        dest: output
""" % VERSION


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

    def default_config(self, args):
        if args.flavor == 'reveal':
            from .reveal import RevealConfig as Config

        config = Config()

        output = sys.stdout

        if args.output:
            output = open(args.output, 'w')
        config.dump(output)
        output.flush()
        if output is not sys.stdout:
            output.close()

    def main(self, argv=sys.argv):
        args = self.parser.parse_args(argv[1:])

        # Python log levels go from 10 (DEBUG) to 50 (CRITICAL),
        # our verbosity argument goes from -1 (-q) to 2 (-vv).
        # We never want to suppress error and critical messages,
        # and default to 30 (WARNING). Hence:
        verbosity = min(args.verbosity, 2)
        loglevel = 30 - (verbosity * 10)
        logging.basicConfig(level=loglevel,
                            format='%(message)s')

        if args.action:
            getattr(self, args.action.replace('-', '_'))(args)


def main(argv=sys.argv):
    try:
        CLI().main(argv)
    except Exception as e:
        logging.error(str(e))
        logging.debug('', exc_info=True)
        try:
            sys.exit(e.errno)
        except AttributeError:
            sys.exit(1)
