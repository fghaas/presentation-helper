from jinja2 import Environment, FileSystemLoader

import yaml

import os

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

    def __init__(self):
        self.setup_argparse()

    def setup_argparse(self):
        options = yaml.load(OPTIONS)

        parser = ArgumentParser()
        sub = parser.add_subparsers(dest='action')

        for cmd, opts in options.items():
            subparser = sub.add_parser(cmd)
            for opt in opts:
                args = opt.pop('flags')
                kwargs = opt
                subparser.add_argument(*args,
                                       **kwargs)

        self.parser = parser
        self.flavor = None
        self.template = None
        self.config = None

    def create(self, args):
        self.flavor = args.flavor

        self.setup_renderer()

        if args.template:
            template_abspath = os.path.abspath(args.template)
            self.setup_template(template_abspath)

        if args.config:
            config_abspath = os.path.abspath(args.config)
            self.setup_config(config_abspath)

        stream = sys.stdout
        if args.output:
            output_abspath = os.path.abspath(args.output)
            stream = open(output_abspath, 'w')

        self.render(stream)

        stream.flush()

    def setup_template(self, path):
        template_dir = os.path.dirname(path)
        template_name = os.path.basename(path)
        env = Environment(loader=FileSystemLoader(template_dir),
                          trim_blocks=True,
                          lstrip_blocks=True)
        self.template = env.get_template(template_name)
        self.setup_renderer()

    def setup_config(self, path):
        with open(path) as config_fd:
            self.config = yaml.load(config_fd)
        self.setup_renderer()

    def setup_renderer(self):
        if self.flavor == 'generic':
            from . import GenericIndexRenderer as Renderer
        elif self.flavor == 'reveal':
            from .reveal import RevealIndexRenderer as Renderer

        self.renderer = Renderer(self.config,
                                 self.template)

    def render(self, stream):
        self.renderer.render_template(stream)

    def main(self, argv=sys.argv):
        args = self.parser.parse_args(argv[1:])

        if args.action:
            getattr(self, args.action)(args)


def main(argv=sys.argv):
    CLI().main(argv)
