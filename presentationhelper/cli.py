from jinja2 import Environment, FileSystemLoader

import yaml

import os

import sys

from argparse import ArgumentParser


class CLI(object):

    def __init__(self):
        self.parser = ArgumentParser()
        self.parser.add_argument('-F',
                                 '--flavor',
                                 default='reveal',
                                 choices=['reveal'],
                                 help="Presentation flavor")
        self.parser.add_argument('-t',
                                 '--template',
                                 metavar='TEMPLATE',
                                 help="Jinja2 template file")
        self.parser.add_argument('-c',
                                 '--config',
                                 metavar='CONFIG',
                                 help="YAML configuration")
        self.parser.add_argument('-o',
                                 '--output',
                                 metavar='OUTPUT',
                                 help="Output file")
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
        from .reveal import RevealIndexRenderer
        self.renderer = RevealIndexRenderer(self.config,
                                            self.template)

    def render(self, stream):
        self.renderer.render_template(stream)

    def main(self, argv=sys.argv[1:]):
        args = self.parser.parse_args(argv)

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
