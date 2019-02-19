# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from jinja2 import Environment, ChoiceLoader, DictLoader, FileSystemLoader

import os

import yaml

import re


class TemplateRendererException(Exception):
    pass


class TemplateRenderer(object):
    """
    Renders an ``index.html`` file from a Jinja2 template, given a set
    of configuration values.

    """

    DEFAULTS = {}

    def __init__(self,
                 config_path=None):
        """Initializes the renderer with a previously loaded Jinja2 template,
        and optionally updates the default values with the given
        config dictionary.

        """
        self._init_config()
        self._setup_config(config_path)
        self._setup_loaders()
        self._load_templates()

    def _init_config(self):
        self.config = self.DEFAULTS.copy()

    def _setup_config(self, config_path=None):
        if config_path:
            with open(config_path, 'r') as config_file:
                self.config.update(yaml.safe_load(config_file))

    def _setup_loaders(self):
        loaders = []
        templates = {}
        try:
            templates = self.config['templates'].copy()
        except KeyError:
            # Config does not contain any template overrides
            pass

        directory = os.getcwd()
        try:
            directory = templates.pop('directory')
        except KeyError:
            # Template overrides does not contain a directory
            pass
        fs_loader = FileSystemLoader(directory)
        loaders.append(fs_loader)

        if templates:
            dict_loader = DictLoader(templates)
            loaders.append(dict_loader)

        self.loaders = loaders

    def _load_templates(self):
        self.templates = []
        loader = ChoiceLoader(self.loaders)
        env = Environment(loader=loader,
                          trim_blocks=True,
                          lstrip_blocks=True)
        template_names = env.list_templates()
        valid_names = [t for t in template_names if t.endswith('.j2')]
        for name in valid_names:
            self.templates.append(env.get_template(name))
        if not self.templates:
            message = "No templates found in %s" % template_names
            raise TemplateRendererException(message)

    def render(self):
        """Renders all loaded templates, using the loaded config."""
        for template in self.templates:
            dest = re.sub('\.j2$', '', template.name)  # noqa: W605
            outfile = os.path.join(os.getcwd(), dest)
            with open(outfile, 'w') as out:
                template.stream(self.config).dump(out)


class PresentationCreator(object):
    """
    Creates a presentation.
    """

    TEMPLATE_RENDERER_CLASS = TemplateRenderer

    def __init__(self, **kwargs):
        """
        :param str config_path: Path to a YAML config file
        :param str template_path: Path to a Jinja2 template
        """

        self.__dict__.update(kwargs)

        self.renderer = self.TEMPLATE_RENDERER_CLASS(**kwargs)

    def create(self):
        self.renderer.render()
