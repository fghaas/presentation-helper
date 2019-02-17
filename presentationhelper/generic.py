from jinja2 import Environment, FileSystemLoader

import sys

import os

import yaml


class IndexRenderer(object):
    """
    Renders an ``index.html`` file from a Jinja2 template, given a set
    of configuration values.

    """

    DEFAULTS = {}

    def __init__(self,
                 config_path=None,
                 template_path=None,
                 output_path=None):
        """Initializes the renderer with a previously loaded Jinja2 template,
        and optionally updates the default values with the given
        config dictionary.

        """
        self._init_config()
        self._setup_config(config_path)
        self._setup_template(template_path)
        self._setup_output(output_path)

    def _init_config(self):
        self.config = self.DEFAULTS.copy()

    def _setup_config(self, config_path=None):
        if config_path:
            with open(config_path, 'r') as config_file:
                self.config.update(yaml.safe_load(config_file))

    def _setup_template(self, template_path=None):
        self.template = None

        if template_path:
            template_dir = os.path.dirname(self.template_path)
            template_name = os.path.basename(self.template_path)
            env = Environment(loader=FileSystemLoader(template_dir),
                              trim_blocks=True,
                              lstrip_blocks=True)
            self.template = env.get_template(template_name)

    def _setup_output(self, output_path=None):
        self.output = sys.stdout
        if output_path:
            self.output = open(output_path, 'w')

    def _update_template(self, template):
        if template:
            self.template = template

    def render(self):
        self.output.write(self.template.render(self.config))
        self.output.flush()

    def __del__(self):
        if self.output is not sys.stdout:
            self.output.close()


class PresentationCreator(object):
    """
    Creates a presentation.
    """

    INDEX_RENDERER_CLASS = IndexRenderer

    def __init__(self, **kwargs):
        """
        :param str config_path: Path to a YAML config file
        :param str template_path: Path to a Jinja2 template
        :param str output_path: Path to the output file or directory
        """

        self.__dict__.update(kwargs)

        self.renderer = self.INDEX_RENDERER_CLASS(**kwargs)

    def create(self):
        self.renderer.render()
