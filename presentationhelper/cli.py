from jinja2 import Environment, FileSystemLoader

import yaml

import os

import sys

from argparse import ArgumentParser


COMMAND = "presentation-helper"


class CLI(object):

    def __init__(self):
        self.setup_argparse()

    def setup_argparse(self):
        parser = ArgumentParser()

        subparsers = parser.add_subparsers(dest='flavor')

        reveal_description = "renders a reveal.js presentation"
        reveal_parser = subparsers.add_parser('reveal',
                                              description=reveal_description)
        reveal_parser.add_argument('-t',
                                   '--template',
                                   metavar='TEMPLATE',
                                   help="Jinja2 template file")
        reveal_parser.add_argument('-c',
                                   '--config',
                                   metavar='CONFIG',
                                   help="YAML configuration")
        reveal_parser.add_argument('-o',
                                   '--output',
                                   metavar='OUTPUT',
                                   help="Output file")

        generic_description = ('renders a presentation '
                               'using a generic Jinja2 template')
        generic_parser = subparsers.add_parser('generic',
                                               description=generic_description)
        generic_parser.add_argument('-t',
                                    '--template',
                                    metavar='TEMPLATE',
                                    help="Jinja2 template file")
        generic_parser.add_argument('-c',
                                    '--config',
                                    metavar='CONFIG',
                                    help="YAML configuration")
        generic_parser.add_argument('-o',
                                    '--output',
                                    metavar='OUTPUT',
                                    help="Output file")
        self.parser = parser

        self.flavor = None
        self.template = None
        self.config = None

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


def main(argv=sys.argv):
    CLI().main(argv)
