# -*- coding: utf-8 -*-
import os

from jinja2 import PackageLoader

from .generic import PresentationCreator as GenericPresentationCreator
from .generic import TemplateRenderer as GenericTemplateRenderer


class RevealTemplateRenderer(GenericTemplateRenderer):

    DEFAULTS = {
        'theme': 'white',
        'highlight': 'github',
        'controls': {
            'enable': True,
            'tutorial': True,
            'layout': 'bottom-right',
            'back_arrows': 'faded',
        },
        'progress': True,
        'show_notes': False,
        'markdown': {
            'path': 'markdown',
            'separator': '^\\n\\n\\n',
            'separator-vertical': '^\\n\\n',
            'separator-notes': '^Note:',
        },
        'sections': [],
    }

    def _setup_loaders(self):
        super(RevealTemplateRenderer, self)._setup_loaders()
        loader = PackageLoader('presentationhelper',
                               os.path.join('templates', 'reveal'))
        self.loaders.append(loader)


class RevealPresentationCreator(GenericPresentationCreator):

    TEMPLATE_RENDERER_CLASS = RevealTemplateRenderer
