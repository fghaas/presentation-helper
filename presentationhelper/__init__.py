#!/usr/bin/env python


class IndexRenderer(object):
    """
    Renders a Jinja2 template, given a set of configuration values.
    """

    DEFAULTS = {}

    def __init__(self, config=None, template=None):
        """Initializes the renderer with a previously loaded Jinja2 template,
        and optionally updates the default values with the given config
        dictionary."""
        self.config = self.DEFAULTS.copy()
        self._update_config(config)
        self._update_template(template)

    def _update_config(self, config):
        if config:
            self.config.update(config)

    def _update_template(self, template):
        if template:
            self.template = template

    def render_template(self, stream):
        stream.write(self.template.render(self.config))
